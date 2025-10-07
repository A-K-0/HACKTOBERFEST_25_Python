"""Metro Platform Monitoring Tool
=================================

Features (current):
  - Person detection (YOLOv8n if available, fallback to HOG)
  - Simple centroid tracking (ID assignment, disappearance pruning)
  - Intrusion detection (crossing a calibrated line)
  - Zone crowd density & alert (configurable polygons & thresholds)
  - Basic CLI interface (choose video source, optionally disable YOLO)

Planned (not implemented in this minimal contribution):
  - Abandoned object detection
  - Fall / posture anomaly detection
  - Queue length estimation, wait-time modeling
  - Violence / aggression detection (temporal patterns)

Controls:
  q  quit | p pause | y YOLO toggle | l line calibrate | ENTER finalize line | r reset line
  z toggle zones | d toggle density alerts | c toggle IDs

Usage:
  python metro_monitor.py --video path/to/video.mp4
  python metro_monitor.py --camera 0  (use webcam)
  python metro_monitor.py --video video.mp4 --no-yolo

Made Hacktoberfest-friendly: single file, clear docstring, easy to extend.
"""
from __future__ import annotations
import argparse, time
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Optional
import cv2, numpy as np

@dataclass
class Track:
    id: int
    centroid: Tuple[int,int]
    last_seen: float = field(default_factory=time.time)
    history: List[Tuple[int,int]] = field(default_factory=list)
    crossed: bool = False

class PeopleDetector:
    def __init__(self, force_no_yolo: bool = False):
        self.hog = cv2.HOGDescriptor(); self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.yolo = None
        self.enabled_yolo = False if force_no_yolo else True
        if self.enabled_yolo:
            self.try_load_yolo()

    def try_load_yolo(self):
        if self.yolo is not None: return
        try:
            from ultralytics import YOLO  # type: ignore
            self.yolo = YOLO("yolov8n.pt")
            print("[INFO] YOLOv8n loaded")
        except Exception as e:
            print(f"[WARN] YOLO load failed: {e}. Falling back to HOG only.")
            self.yolo=None; self.enabled_yolo=False

    def detect(self, frame) -> List[Tuple[int,int,int,int]]:
        boxes: List[Tuple[int,int,int,int]] = []
        if self.enabled_yolo and self.yolo is not None:
            try:
                res = self.yolo(frame, verbose=False)
                for r in res:
                    if not hasattr(r, 'boxes'): continue
                    for b in r.boxes:
                        cls = int(getattr(b,'cls',[0])[0]) if hasattr(b,'cls') else 0
                        if cls == 0:
                            x1,y1,x2,y2 = b.xyxy[0].cpu().numpy().astype(int)
                            boxes.append((x1,y1,x2-x1,y2-y1))
            except Exception as e:
                print(f"[ERR] YOLO inference error: {e}")
        if not boxes: # fallback to HOG if empty
            scale=0.6
            resized = cv2.resize(frame,(int(frame.shape[1]*scale),int(frame.shape[0]*scale)))
            rects,_ = self.hog.detectMultiScale(resized, winStride=(4,4), padding=(8,8), scale=1.05)
            for (x,y,w,h) in rects:
                boxes.append((int(x/scale), int(y/scale), int(w/scale), int(h/scale)))
        return boxes

class MetroMonitor:
    def __init__(self, src: str | int, force_no_yolo: bool=False):
        self.cap = cv2.VideoCapture(src)
        if not self.cap.isOpened():
            raise SystemExit(f"[ERROR] Cannot open source: {src}")
        self.detector = PeopleDetector(force_no_yolo=force_no_yolo)
        self.tracks: Dict[int,Track] = {}; self.next_id=1; self.max_disappeared=2.0
        self.line_points: List[Tuple[int,int]] = []; self.calibrating_line=False
        self.zones: List[Tuple[str,List[Tuple[int,int]], float]] = []
        self.show_zones=True; self.enable_density=True; self.show_ids=True
        ret, frame = self.cap.read()
        if ret:
            h,w=frame.shape[:2]
            platform = [(int(w*0.05), int(h*0.4)), (int(w*0.95), int(h*0.4)), (int(w*0.95), int(h*0.95)), (int(w*0.05), int(h*0.95))]
            self.zones.append(("PLATFORM", platform, 0.00025))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,0)

    # --- Mouse ---
    def mouse(self,event,x,y,flags,param):
        if self.calibrating_line and event==cv2.EVENT_LBUTTONDOWN:
            self.line_points.append((x,y))
        elif self.calibrating_line and event==cv2.EVENT_RBUTTONDOWN and self.line_points:
            self.line_points.pop()

    # --- Tracking ---
    def update_tracks(self, detections: List[Tuple[int,int,int,int]]):
        centroids = [(x+w//2, y+h//2, (x,y,w,h)) for (x,y,w,h) in detections]
        used=set(); now=time.time()
        for cx,cy,box in centroids:
            best=None; bestd=99999
            for tid,tr in self.tracks.items():
                if tid in used: continue
                d=(tr.centroid[0]-cx)**2+(tr.centroid[1]-cy)**2
                if d<bestd and d<200**2: bestd=d; best=tid
            if best is None:
                self.tracks[self.next_id]=Track(id=self.next_id, centroid=(cx,cy), history=[(cx,cy)])
                self.next_id+=1
            else:
                tr=self.tracks[best]; tr.centroid=(cx,cy); tr.history.append((cx,cy)); tr.last_seen=now; used.add(best)
        # remove stale
        drop=[tid for tid,tr in self.tracks.items() if now-tr.last_seen>self.max_disappeared]
        for tid in drop: del self.tracks[tid]

    # --- Line helpers ---
    def interp_line_y(self, x:int)->Optional[float]:
        if len(self.line_points)<2: return None
        pts=sorted(self.line_points,key=lambda p:p[0])
        for i in range(len(pts)-1):
            x1,y1=pts[i]; x2,y2=pts[i+1]
            if x1<=x<=x2 or x2<=x<=x1:
                if x2!=x1:
                    t=(x-x1)/(x2-x1)
                    return y1 + t*(y2-y1)
                return (y1+y2)/2
        return None

    def detect_intrusions(self, frame):
        if len(self.line_points)<2: return []
        intr=[]
        for tid,tr in self.tracks.items():
            if tr.crossed: continue
            y_line=self.interp_line_y(tr.centroid[0])
            if y_line is None: continue
            if tr.centroid[1] > y_line + 10:
                tr.crossed=True; intr.append(tid)
                cv2.putText(frame,"INTRUSION!",(tr.centroid[0]-40,tr.centroid[1]-25),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)
        return intr

    def zone_density(self, detections):
        out=[]
        for name,poly,thresh in self.zones:
            cnt=np.array(poly,np.int32); area=cv2.contourArea(cnt)
            c=0
            for (x,y,w,h) in detections:
                cx=float(x+w//2); cy=float(y+h//2)
                if cv2.pointPolygonTest(cnt.astype(np.float32),(cx,cy),False)>=0: c+=1
            dens=c/area if area>0 else 0
            over=dens>thresh and self.enable_density
            out.append((name,c,dens,thresh,over))
        return out

    # --- Main ---
    def run(self):
        paused=False
        cv2.namedWindow("MetroMonitor")
        cv2.setMouseCallback("MetroMonitor", self.mouse)
        while True:
            if not paused:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES,0); continue
            disp=frame.copy()
            dets=self.detector.detect(frame)
            self.update_tracks(dets)

            # zones
            if self.show_zones:
                for name,poly,_ in self.zones:
                    cv2.polylines(disp,[np.array(poly,np.int32)],True,(60,120,255),2)
                    cv2.putText(disp,name,(poly[0][0],poly[0][1]-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(60,120,255),1)

            # line
            if len(self.line_points)>=2:
                cv2.polylines(disp,[np.array(self.line_points,np.int32)],False,(0,0,255),3)
                for p in self.line_points: cv2.circle(disp,p,4,(0,0,255),-1)
                if self.calibrating_line:
                    cv2.putText(disp,f"Line pts: {len(self.line_points)} (ENTER to save)",(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.55,(0,255,255),2)

            # det boxes
            for (x,y,w,h) in dets: cv2.rectangle(disp,(x,y),(x+w,y+h),(0,255,0),2)
            for tid,tr in self.tracks.items():
                col=(0,0,255) if tr.crossed else (255,255,0)
                cv2.circle(disp,tr.centroid,5,col,-1)
                if self.show_ids: cv2.putText(disp,f"ID{tid}",(tr.centroid[0]+6,tr.centroid[1]-6),cv2.FONT_HERSHEY_SIMPLEX,0.4,col,1)

            intr=self.detect_intrusions(disp)
            densities=self.zone_density(dets)

            # panel
            cv2.rectangle(disp,(10,10),(340,120),(0,0,0),-1)
            cv2.rectangle(disp,(10,10),(340,120),(255,255,255),1)
            cv2.putText(disp,f"Tracks: {len(self.tracks)}",(20,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
            for i,(name,c,d,th,over) in enumerate(densities[:3]):
                cv2.putText(disp,f"{name}: {c} ({d*1000:.2f}k)",(20,50+18*i),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,255,0) if not over else (0,0,255),1)
                if over:
                    cv2.putText(disp,"DENSITY ALERT",(180,50+18*i),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,0,255),1)
            if intr: cv2.putText(disp,f"INTRUSIONS: {len(intr)}",(20,110),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)

            cv2.putText(disp,"q quit|p pause|y YOLO|l line|z zones|d density|c IDs",(20,disp.shape[0]-15),cv2.FONT_HERSHEY_SIMPLEX,0.45,(255,255,255),1)
            cv2.imshow("MetroMonitor",disp)
            k=cv2.waitKey(1) & 0xFF
            if k==ord('q'): break
            elif k==ord('p'): paused=not paused
            elif k==ord('y'):
                if self.detector.enabled_yolo and self.detector.yolo is not None:
                    self.detector.enabled_yolo=False; print("[INFO] YOLO disabled -> HOG only")
                else:
                    print("[INFO] Enabling YOLO..."); self.detector.enabled_yolo=True; self.detector.try_load_yolo()
            elif k==ord('l'):
                self.calibrating_line=not self.calibrating_line
                if self.calibrating_line:
                    self.line_points=[]; print("[CAL] Click to add points; ENTER to finalize")
            elif k==13 and self.calibrating_line:
                self.calibrating_line=False; print(f"[CAL] Line saved with {len(self.line_points)} points")
            elif k==ord('r'):
                self.line_points=[]; print("[CAL] Line reset")
            elif k==ord('z'): self.show_zones=not self.show_zones
            elif k==ord('d'): self.enable_density=not self.enable_density
            elif k==ord('c'): self.show_ids=not self.show_ids
        self.cap.release(); cv2.destroyAllWindows()


def parse_args():
    ap=argparse.ArgumentParser(description="Metro platform monitoring (intrusion + density)")
    gsrc=ap.add_mutually_exclusive_group(required=True)
    gsrc.add_argument('--video', type=str, help='Path to video file')
    gsrc.add_argument('--camera', type=int, help='Camera index (e.g. 0)')
    ap.add_argument('--no-yolo', action='store_true', help='Force disable YOLO (use HOG only)')
    return ap.parse_args()

if __name__ == '__main__':
    args=parse_args()
    source = args.video if args.video else args.camera
    monitor=MetroMonitor(source, force_no_yolo=args.no_yolo)
    monitor.run()
