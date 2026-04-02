import numpy as np
import pytest
from monitor import RegionMonitor

@pytest.fixture
def monitor():
 cfg = {
 "color_threshold": 15,
 "regions": [
 {"name": "red", "x": 10, "y": 10, "w": 20, "h": 20,
 "target_color": [255, 0, 0], "tolerance": 15},
 ],
 }
 return RegionMonitor(cfg)

@pytest.fixture
def frame():
 return np.zeros((100, 100, 3), dtype=np.uint8)

def test_no_detection(monitor, frame):
 results = monitor.analyze(frame)
 assert len(results) == 0

def test_detect_red(monitor, frame):
 frame[15, 15] = [255, 0, 0]
 # Need multiple frames for stability
 for _ in range(5):
 results = monitor.analyze(frame)
 assert len(results) >= 1
 assert results[0]["region"] == "red"

def test_tolerance(monitor, frame):
 frame[15, 15] = [245, 5, 5] # close to red
 for _ in range(5):
 results = monitor.analyze(frame)
 assert len(results) >= 1

def test_out_of_bounds(monitor, frame):
 monitor.regions.append(
 {"name": "oob", "x": 999, "y": 999, "w": 10, "h": 10,
 "target_color": [0, 0, 0], "tolerance": 5}
 )
 results = monitor.analyze(frame)
 assert not any(r["region"] == "oob" for r in results)
