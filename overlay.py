import tkinter as tk
import threading
import logging

log = logging.getLogger(__name__)

class OverlayWindow:
 """Transparent overlay with crosshair and detection boxes."""

 STYLES = {"dot": "_draw_dot", "cross": "_draw_cross", "circle": "_draw_circle"}

 def __init__(self, cfg: dict):
 self.cfg = cfg
 self._visible = cfg.get("enabled", True)
 self._style = cfg.get("crosshair", "dot")
 self._color = cfg.get("color", "#FF0000")
 self._size = cfg.get("size", 10)
 self._opacity = cfg.get("opacity", 0.8)
 self._detections = []
 self._fps = 0.0
 self._root = None
 self._canvas = None
 self._close_event = threading.Event()

 def run(self):
 self._root = tk.Tk()
 self._root.overrideredirect(True)
 self._root.attributes("-topmost", True)
 self._root.attributes("-alpha", self._opacity)
 w = self._root.winfo_screenwidth()
 h = self._root.winfo_screenheight()
 self._root.geometry(f"{w}x{h}+0+0")
 self._root.configure(bg="black")
 self._root.attributes("-transparentcolor", "black")
 self._canvas = tk.Canvas(self._root, bg="black", highlightthickness=0)
 self._canvas.pack(fill=tk.BOTH, expand=True)
 self._draw()
 self._root.mainloop()
 self._close_event.set()

 def _draw(self):
 if not self._canvas:
 return
 self._canvas.delete("all")
 if self._visible:
 w = self._root.winfo_screenwidth()
 h = self._root.winfo_screenheight()
 cx, cy = w // 2, h // 2
 fn = getattr(self, self.STYLES.get(self._style, "_draw_dot"))
 fn(cx, cy)
 for det in self._detections:
 x, y = det.get("x", 0), det.get("y", 0)
 self._canvas.create_rectangle(
 x - 5, y - 5, x + 5, y + 5, outline="#00FF00", width=2
 )
 self._canvas.create_text(
 10, 10, text=f"FPS: {int(self._fps)}", fill="white",
 anchor="nw", font=("Consolas", 9),
 )
 self._root.after(16, self._draw)

 def _draw_dot(self, cx, cy):
 s = self._size // 2
 self._canvas.create_oval(cx - s, cy - s, cx + s, cy + s,
 fill=self._color, outline=self._color)

 def _draw_cross(self, cx, cy):
 s = self._size
 self._canvas.create_line(cx - s, cy, cx + s, cy, fill=self._color, width=2)
 self._canvas.create_line(cx, cy - s, cx, cy + s, fill=self._color, width=2)

 def _draw_circle(self, cx, cy):
 s = self._size
 self._canvas.create_oval(cx - s, cy - s, cx + s, cy + s,
 outline=self._color, width=2)

 def update(self, detections, fps):
 self._detections = detections
 self._fps = fps

 def toggle(self):
 self._visible = not self._visible

 def hide(self):
 self._visible = False

 def close(self):
 if self._root:
 self._root.quit()

 def wait(self):
 self._close_event.wait()
