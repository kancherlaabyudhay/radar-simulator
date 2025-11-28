import matplotlib.pyplot as plt
from src.pulse import generate_rect_pulse
from src.noise import add_noise
from src.detect import threshold_detect, extract_segments, group_close_segments, hysteresis_detect
from src.filter import matched_filter

if __name__ == "__main__":
    fs = 5000
    duration = 0.6
    start = 0.18
    end = 0.22
    noise_sigma = 0.25
    threshold = 0.5
    gap_threshold = 0.005

    t, pulse = generate_rect_pulse(fs, duration, start, end)
    signal = add_noise(pulse, sigma=noise_sigma)

    # matched filter output (normalized)
    mf_out = matched_filter(signal, pulse)

    # detection on matched filter output (use lower threshold because mf_out normalized)
    mf_threshold = 0.3
    mf_detections = threshold_detect(mf_out, mf_threshold)
    mf_segs = extract_segments(mf_detections, t)
    mf_grouped = group_close_segments(mf_segs, gap_threshold)

    # also compute hysteresis on raw signal for comparison
    hyster = hysteresis_detect(signal, low_thresh=0.3, high_thresh=0.6)
    hyster_segs = extract_segments(hyster, t)
    hyster_grouped = group_close_segments(hyster_segs, gap_threshold)

    plt.figure(figsize=(12, 8))

    plt.subplot(3, 1, 1)
    plt.plot(t, signal, label="raw signal")
    plt.axvspan(start, end, color="green", alpha=0.08, label="true pulse")
    plt.title("Raw Noisy Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(t, mf_out, label="matched filter output")
    plt.axhline(mf_threshold, linestyle="--", label="mf threshold")
    for s, e in mf_grouped:
        plt.axvspan(s, e, color="orange", alpha=0.2)
    plt.title("Matched Filter Output (normalized)")
    plt.xlabel("Time (s)")
    plt.ylabel("Normalized amplitude")
    plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(t, signal, label="raw signal")
    plt.plot(t[mf_detections], signal[mf_detections], "o", markersize=3, label="mf hits")
    plt.plot(t[hyster], signal[hyster], "x", markersize=3, label="hysteresis state (raw)")
    plt.title("Detections Comparison")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()

    plt.tight_layout()
    plt.show()

    print("Matched filter grouped segments:", mf_grouped)
    print("Hysteresis grouped segments:", hyster_grouped)
