import numpy as np
import logging
from dataclasses import dataclass

log = logging.getLogger(__name__)

@dataclass
class Detection:
 region: str
 x: int
 y: int
 confidence: float

class RegionMonitor:
 """Pixel-based screen region monitor with numpy vectorized ops."""

 def __init__(self, cfg: dict):
 self.regions = cfg.get("regions", [])
 self.threshold = cfg.get("color_threshold", 15)
 self.min_area = cfg.get("min_area", 10)
 self._history: dict[str, list] = {}

 def analyze(self, frame: np.ndarray) -> list[dict]:
 results = []
 for region in self.regions:
 name = region.get("name", "default")
 x, y = region.get("x", 0), region.get("y", 0)
 w, h = region.get("w", 50), region.get("h", 50)
 target = np.array(region.get("target_color", [255, 0, 0]), dtype=np.float32)
 tol = region.get("tolerance", self.threshold)

 # Bounds check
 y1, y2 = max(0, y), min(frame.shape[0], y + h)
 x1, x2 = max(0, x), min(frame.shape[1], x + w)
 if y2 <= y1 or x2 <= x1:
 continue

 roi = frame[y1:y2, x1:x2].astype(np.float32)
 dist = np.sqrt(np.sum((roi - target) ** 2, axis=-1))
 mask = dist <= tol

 if np.any(mask):
 match_y, match_x = np.where(mask)
 cx = int(np.mean(match_x)) + x1
 cy = int(np.mean(match_y)) + y1
 conf = float(np.mean(mask))

 # Stability filter
 hist = self._history.setdefault(name, [])
 hist.append(True)
 if len(hist) > 5:
 hist.pop(0)
 if sum(hist) >= 3:
 results.append({"region": name, "x": cx, "y": cy, "confidence": conf})
 else:
 hist = self._history.setdefault(name, [])
 hist.append(False)
 if len(hist) > 5:
 hist.pop(0)

 return results
