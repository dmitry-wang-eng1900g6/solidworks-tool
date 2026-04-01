import hashlib
import shutil
import logging
from pathlib import Path

log = logging.getLogger(__name__)

def file_hash(path: str) -> str:
 h = hashlib.sha256()
 with open(path, "rb") as f:
 for chunk in iter(lambda: f.read(8192), b""):
 h.update(chunk)
 return h.hexdigest()

def backup_file(path: Path):
 backup_dir = path.parent / ".backup"
 backup_dir.mkdir(exist_ok=True)
 dest = backup_dir / path.name
 shutil.copy2(path, dest)
 log.info("Backup: %s → %s", path.name, dest)

def restore_file(backup: Path, target: Path):
 shutil.copy2(backup, target)
 log.info("Restored: %s", target.name)
