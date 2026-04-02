import yaml
import os
import logging

log = logging.getLogger(__name__)

DEFAULT_CONFIG = {
 "": {"fps": 60, "monitor": 0},
 "detection": {
 "color_threshold": 15,
 "min_area": 10,
 "regions": [
 {"name": "center", "x": 900, "y": 500, "w": 120, "h": 80,
 "target_color": [255, 0, 0], "tolerance": 20},
 ],
 },
 "overlay": {
 "enabled": True, "crosshair": "dot",
 "color": "#FF0000", "size": 10, "opacity": 0.8,
 },
 "hotkeys": {
 "toggle": "f1", "overlay": "f2",
 "reload": "f3", "exit": "delete",
 },
}

def load_config(path: str = "config.yaml") -> dict:
 if not os.path.exists(path):
 log.info("Config not found, creating default: %s", path)
 save_config(DEFAULT_CONFIG, path)
 return dict(DEFAULT_CONFIG)
 with open(path, "r") as f:
 cfg = yaml.safe_load(f) or {}
 merged = {**DEFAULT_CONFIG, **cfg}
 return merged

def save_config(cfg: dict, path: str = "config.yaml"):
 with open(path, "w") as f:
 yaml.dump(cfg, f, default_flow_style=False)
 log.info("Config saved: %s", path)
