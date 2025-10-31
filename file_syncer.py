"""
file_syncer.py — Sync files between folders with SHA256 verification.
"""
import os, shutil, hashlib, logging, argparse
from pathlib import Path


def setup_logger():
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


def sha256sum(file_path: Path) -> str:
h = hashlib.sha256()
with open(file_path, "rb") as f:
for chunk in iter(lambda: f.read(8192), b""):
h.update(chunk)
return h.hexdigest()


def sync_files(src_dir: Path, dst_dir: Path):
if not src_dir.exists():
logging.error(f"Source not found: {src_dir}")
return
dst_dir.mkdir(parents=True, exist_ok=True)
copied, skipped = 0, 0
for file in src_dir.rglob("*"):
if file.is_file():
dest = dst_dir / file.relative_to(src_dir)
dest.parent.mkdir(parents=True, exist_ok=True)
if dest.exists() and sha256sum(file) == sha256sum(dest):
skipped += 1; continue
shutil.copy2(file, dest)
copied += 1; logging.info(f"Copied: {file.name}")
logging.info(f"✅ Sync done: {copied} copied, {skipped} skipped.")


def main():
setup_logger()
parser = argparse.ArgumentParser(description="Sync files between folders.")
parser.add_argument("--src", required=True)
parser.add_argument("--dst", required=True)
args = parser.parse_args()
sync_files(Path(args.src), Path(args.dst))
if __name__ == "__main__": main()
