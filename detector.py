import os
import logging
from pathlib import Path

log = logging.getLogger(__name__)

SEARCH_PATHS = [
 Path(os.environ.get("PROGRAMFILES", "C:/Program Files")),
 Path(os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")),
 Path(os.environ.get("LOCALAPPDATA", "")),
 Path(os.environ.get("APPDATA", "")),
]

def detect_installation(cfg: dict) -> Path | None:
 custom_path = cfg.get("target", {}).get("path")
 if custom_path and custom_path != "auto":
 p = Path(custom_path)
 if p.exists():
 log.info("Using custom path: %s", p)
 return p

 target_name = cfg.get("target", {}).get("name", "solidworks")
 for base in SEARCH_PATHS:
 if not base.exists():
 continue
 for d in base.iterdir():
 if target_name.lower() in d.name.lower() and d.is_dir():
 log.info("Found installation: %s", d)
 return d

 log.warning("Installation not found in standard paths")
 return None
