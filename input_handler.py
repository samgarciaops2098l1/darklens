import logging
import threading
from typing import Callable

log = logging.getLogger(__name__)

class HotkeyManager:
 """Keyboard hotkey handler using pynput."""

 def __init__(self):
 self._bindings: dict = {}
 self._listener = None

 def register(self, key_name: str, callback: Callable):
 self._bindings[key_name.lower()] = callback

 def listen(self):
 try:
 from pynput import keyboard

 def on_press(key):
 try:
 name = key.name if hasattr(key, "name") else str(key.char)
 if name.lower() in self._bindings:
 self._bindings[name.lower()]()
 except Exception as e:
 log.debug("Hotkey error: %s", e)

 self._listener = keyboard.Listener(on_press=on_press)
 self._listener.start()
 self._listener.join()
 except ImportError:
 log.warning("pynput not available — hotkeys disabled")
 threading.Event().wait()

 def stop(self):
 if self._listener:
 self._listener.stop()
