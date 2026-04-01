import yaml
import os
import logging

log = logging.getLogger(__name__)

DEFAULT_CONFIG = {
 "target": {"path": "auto", "name": "", "version": "latest"},
 "es": [
 {"file": "app.dll", "original": "4A6F686E", "": "4A6F686E"},
 ],
 "backup": True,
 "verify": True,
}

def load_config(path: str = "config.yaml") -> dict:
 if not os.path.exists(path):
 save_config(DEFAULT_CONFIG, path)
 return dict(DEFAULT_CONFIG)
 with open(path) as f:
 return {**DEFAULT_CONFIG, **(yaml.safe_load(f) or {})}

def save_config(cfg: dict, path: str = "config.yaml"):
 with open(path, "w") as f:
 yaml.dump(cfg, f, default_flow_style=False)
