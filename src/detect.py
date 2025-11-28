import numpy as np

def threshold_detect(signal, threshold):
    return signal > threshold

def extract_segments(detections, time_axis):
    segments = []
    in_seg = False
    start = None
    for i, val in enumerate(detections):
        if val and not in_seg:
            in_seg = True
            start = i
        if not val and in_seg:
            in_seg = False
            end = i - 1
            segments.append((start, end))
    if in_seg:
        segments.append((start, len(detections)-1))
    return [(time_axis[s], time_axis[e]) for s, e in segments]

def group_close_segments(segments, gap_thresh):
    if not segments:
        return []
    grouped = []
    cur_start, cur_end = segments[0]
    for s, e in segments[1:]:
        if s - cur_end <= gap_thresh:
            cur_end = e
        else:
            grouped.append((cur_start, cur_end))
            cur_start, cur_end = s, e
    grouped.append((cur_start, cur_end))
    return grouped

def hysteresis_detect(signal, low_thresh, high_thresh):
    state = False
    out = np.zeros_like(signal, dtype=bool)
    for i, v in enumerate(signal):
        if not state and v > high_thresh:
            state = True
        elif state and v < low_thresh:
            state = False
        out[i] = state
    return out
