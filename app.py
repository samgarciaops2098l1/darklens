#!/usr/bin/env python3
"""Pubg: screen analysis tool with overlay and hotkeys."""
import argparse
import logging
import threading
import time
import numpy as np
from mss import mss
from config import load_config
from monitor import RegionMonitor
from overlay import OverlayWindow
from input_handler import HotkeyManager

log = logging.getLogger(__name__)

class Darklens:
 def __init__(self, config_path: str = "config.yaml"):
 self.cfg = load_config(config_path)
 self.active = threading.Event()
 self.active.set()
 self.monitor = RegionMonitor(self.cfg.get("detection", {}))
 self.overlay = OverlayWindow(self.cfg.get("overlay", {}))
 self.hotkeys = HotkeyManager()
 self._setup_hotkeys()

 def _setup_hotkeys(self):
 keys = self.cfg.get("hotkeys", {})
 self.hotkeys.register(keys.get("toggle", "f1"), self._toggle)
 self.hotkeys.register(keys.get("overlay", "f2"), self.overlay.toggle)
 self.hotkeys.register(keys.get("exit", "delete"), self._exit)

 def _toggle(self):
 if self.active.is_set():
 self.active.clear()
 log.info("Paused")
 else:
 self.active.set()
 log.info("Resumed")

 def _exit(self):
 self.active.clear()
 self.overlay.hide()
 log.info("Exit — closed")

 def __loop(self):
 sct = mss()
 fps = self.cfg.get("", {}).get("fps", 60)
 frame_time = 1.0 / fps
 while not self._stop.is_set():
 t0 = time.perf_counter()
 frame = np.array(sct.grab(sct.monitors[0]))[:, :, :3]
 if self.active.is_set():
 detections = self.monitor.analyze(frame)
 self.overlay.update(detections, 1.0 / max(time.perf_counter() - t0, 0.001))
 elapsed = time.perf_counter() - t0
 if elapsed < frame_time:
 time.sleep(frame_time - elapsed)

 def start(self):
 log.info("darklens starting...")
 self._stop = threading.Event()
 threading.Thread(target=self.hotkeys.listen, daemon=True).start()
 threading.Thread(target=self.__loop, daemon=True).start()
 try:
 self.overlay.run()
 except KeyboardInterrupt:
 pass
 finally:
 self.stop()

 def stop(self):
 self._stop.set()
 self.overlay.close()
 self.hotkeys.stop()
 log.info("darklens stopped")

def main():
 parser = argparse.ArgumentParser(description=__doc__)
 parser.add_argument("-c", "--config", default="config.yaml")
 parser.add_argument("-v", "--verbose", action="store_true")
 args = parser.parse_args()
 logging.basicConfig(
 level=logging.DEBUG if args.verbose else logging.INFO,
 format="%(asctime)s [%(levelname)s] %(message)s",
 )
 app = Darklens(args.config)
 app.start()

if __name__ == "__main__":
 main()
