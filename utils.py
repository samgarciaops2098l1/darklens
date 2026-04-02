import hashlib
import logging
import time
from pathlib import Path

log = logging.getLogger(__name__)

def file_hash(path: str) -> str:
 h = hashlib.sha256()
 with open(path, "rb") as f:
 for chunk in iter(lambda: f.read(8192), b""):
 h.update(chunk)
 return h.hexdigest()

def timer(label: str = ""):
 class _Timer:
 def __enter__(self):
 self.t0 = time.perf_counter()
 return self
 def __exit__(self, *args):
 ms = (time.perf_counter() - self.t0) * 1000
 log.debug("%s: %.1fms", label or "timer", ms)
 return _Timer()

def ensure_dir(path: str) -> Path:
 p = Path(path)
 p.mkdir(parents=True, exist_ok=True)
 return p
