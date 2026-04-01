#!/usr/bin/env python3
"""Solidworks configuion tool — es target application."""
import argparse
import logging
import sys
from pathlib import Path
from config import load_config
from detector import detect_installation
from utils import backup_file, restore_file, file_hash

log = logging.getLogger(__name__)

def apply_(target_dir: Path, cfg: dict) -> bool:
 log.info("Scanning %s...", target_dir)
 es = cfg.get("es", [])
 if not es:
 log.error("No update definitions in config")
 return False

 for update in es:
 target_file = target_dir / update["file"]
 if not target_file.exists():
 log.warning("Target not found: %s", target_file)
 continue

 if cfg.get("backup", True):
 backup_file(target_file)

 data = target_file.read_bytes()
 original = bytes.fromhex(update["original"])
 replacement = bytes.fromhex(update["utility"])

 if original not in data:
 log.info("Already utility or wrong version: %s", target_file.name)
 continue

 utility = data.replace(original, replacement, 1)
 target_file.write_bytes(utility)
 log.info("utility: %s", target_file.name)

 return True

def rollback(target_dir: Path) -> bool:
 backup_dir = target_dir / ".backup"
 if not backup_dir.exists():
 log.error("No backup found")
 return False
 for bak in backup_dir.glob("*"):
 dest = target_dir / bak.name
 dest.write_bytes(bak.read_bytes())
 log.info("Restored: %s", bak.name)
 return True

def main():
 parser = argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--apply", action="store_true", help="Apply update")
 parser.add_argument("--rollback", action="store_true", help="Undo update")
 parser.add_argument("--status", action="store_true", help="Check status")
 parser.add_argument("-c", "--config", default="config.yaml")
 parser.add_argument("-v", "--verbose", action="store_true")
 args = parser.parse_args()

 logging.basicConfig(
 level=logging.DEBUG if args.verbose else logging.INFO,
 format="%(asctime)s [%(levelname)s] %(message)s",
 )

 cfg = load_config(args.config)
 target = detect_installation(cfg)
 if not target:
 log.error("Could not find solidworks installation")
 sys.exit(1)

 if args.apply:
 ok = apply_(target, cfg)
 sys.exit(0 if ok else 1)
 elif args.rollback:
 ok = rollback(target)
 sys.exit(0 if ok else 1)
 elif args.status:
 log.info("Installation: %s", target)
 log.info("Hash: %s", file_hash(str(target / cfg["es"][0]["file"])))
 else:
 parser.print_help()

if __name__ == "__main__":
 main()
