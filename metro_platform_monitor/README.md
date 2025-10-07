# Metro Platform Monitor

A Hacktoberfest-friendly computer vision project for monitoring metro / train platforms.

## Features (Current)
- Person detection (YOLOv8n if installed, fallback to HOG pedestrian detector)
- Simple centroid tracking (assign IDs, prune disappeared)
- Intrusion detection (crossing a calibrated virtual safety line)
- Zone-based crowd density and alerting (configurable polygons & thresholds)
- Keyboard interactive calibration & toggles

## Planned / Stretch Ideas
- Abandoned object detection (stationary non-person for N seconds)
- Fall / posture anomaly detection (pose estimation based)
- Queue length & wait-time estimation (ordered centroids in queue polygon)
- Violence / aggression detection (temporal motion signatures)
- Persistence of calibration (save/load JSON)

## Quick Start
```bash
python metro_monitor.py --video path/to/platform_video.mp4
# or use a webcam
python metro_monitor.py --camera 0
```
Optional (install YOLO for better accuracy):
```bash
pip install ultralytics
```
Disable YOLO explicitly:
```bash
python metro_monitor.py --video video.mp4 --no-yolo
```

## Controls
| Key | Action |
|-----|--------|
| q | Quit |
| p | Pause/resume |
| y | Toggle / load YOLO |
| l | Start/stop safety line calibration |
| ENTER | Finalize line during calibration |
| r | Reset line |
| z | Toggle zone drawing |
| d | Toggle density alerts |
| c | Toggle track ID display |
| Left Click | Add line point while calibrating |
| Right Click | Remove last line point while calibrating |

## Adjusting Zones & Thresholds
Edit the list `self.zones` inside `MetroMonitor.__init__`. Each zone tuple:
```python
(name, [(x1,y1), (x2,y2), ...], density_threshold_people_per_pixel)
```
Density is computed as `people_count / zone_pixel_area`. A zone triggers an alert if density > threshold and alerts are enabled.

## Contributing
Feel free to add any planned feature or improvements:
- Implement abandoned object tracking (background model + stationary timer)
- Add JSON persistence for line & zones
- Integrate pose detection for fall detection
- Add a queue analytics module

Please follow repository contribution guidelines and include a brief README update.

## License
MIT
