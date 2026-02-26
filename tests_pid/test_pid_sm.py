import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PID_SM import PID


def test_pid_output_increases_when_below_setpoint():
    pid = PID(rate=0.01, kp=2.0, ki=0.3, kd=0.0)
    time.sleep(0.02)
    output = pid.compute(Input=85.0, Setpoint=93.0)
    assert output > 0


def test_pid_output_clamped_to_output_limits():
    pid = PID(rate=0.01, kp=100.0, ki=20.0, kd=0.0)
    pid.SetOutputLimits(0, 60)
    time.sleep(0.02)
    output = pid.compute(Input=20.0, Setpoint=93.0)
    assert 0 <= output <= 60


def test_safety_cutoff_sets_output_to_zero_on_overtemp():
    pid = PID(rate=0.01, kp=2.0, ki=1.0, kd=0.0)
    time.sleep(0.02)
    _ = pid.compute(Input=80.0, Setpoint=93.0)
    time.sleep(0.02)
    output = pid.compute(Input=96.5, Setpoint=93.0)
    assert output == 0
