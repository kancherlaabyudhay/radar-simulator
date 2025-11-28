import numpy as np
from .timebase import generate_time_axis

def generate_rect_pulse(fs, duration, start, end, amplitude=1.0):
    t = generate_time_axis(fs, duration)
    pulse = np.zeros_like(t)
    pulse[(t >= start) & (t < end)] = amplitude
    return t, pulse
