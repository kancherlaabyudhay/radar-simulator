import numpy as np
import matplotlib.pyplot as plt
from src.pulse import generate_rect_pulse
from src.noise import add_noise
from src.filter import matched_filter
from src.detect import threshold_detect, extract_segments, group_close_segments

def eval_single_run(fs, duration, start, end, noise_sigma, mf_threshold, gap_threshold):
    t, pulse = generate_rect_pulse(fs, duration, start, end)
    signal = add_noise(pulse, sigma=noise_sigma)
    mf_out = matched_filter(signal, pulse)
    detections = threshold_detect(mf_out, mf_threshold)
    segs = extract_segments(detections, t)
    grouped = group_close_segments(segs, gap_threshold)
    # classify grouped segments
    true_window = (start, end)
    tp_found = False
    false_alarms = 0
    latencies = []
    dur_errors = []
    for s, e in grouped:
        overlap = not (e < true_window[0] or s > true_window[1])
        if overlap and not tp_found:
            tp_found = True
            latency = s - true_window[0]
            dur_error = abs((e - s) - (true_window[1] - true_window[0]))
            latencies.append(latency)
            dur_errors.append(dur_error)
        elif not overlap:
            false_alarms += 1
    return tp_found, false_alarms, (latencies[0] if latencies else None), (dur_errors[0] if dur_errors else None)

def run_grid(fs=5000, duration=0.6, start=0.18, end=0.22,
             noise_list=None, mf_thresh_list=None, gap_threshold=0.005,
             trials=100):
    if noise_list is None:
        noise_list = np.linspace(0.05, 0.5, 10)  # try noise sigma from low to high
    if mf_thresh_list is None:
        mf_thresh_list = np.linspace(0.15, 0.6, 10)  # matched filter thresholds to try

    results = np.zeros((len(noise_list), len(mf_thresh_list)), dtype=[('tp_rate','f8'), ('false_alarm','f8'),
                                                                       ('latency','f8'), ('dur_err','f8')])

    for i, ns in enumerate(noise_list):
        for j, mf_th in enumerate(mf_thresh_list):
            tp_count = 0
            false_sum = 0
            lat_sum = 0.0
            dur_sum = 0.0
            lat_count = 0
            dur_count = 0
            for _ in range(trials):
                tp, fa, lat, de = eval_single_run(fs, duration, start, end, ns, mf_th, gap_threshold)
                if tp:
                    tp_count += 1
                    if lat is not None:
                        lat_sum += lat
                        lat_count += 1
                    if de is not None:
                        dur_sum += de
                        dur_count += 1
                false_sum += fa
            tp_rate = tp_count / trials
            avg_false = false_sum / trials
            avg_lat = (lat_sum / lat_count) if lat_count>0 else np.nan
            avg_de = (dur_sum / dur_count) if dur_count>0 else np.nan
            results[i, j]['tp_rate'] = tp_rate
            results[i, j]['false_alarm'] = avg_false
            results[i, j]['latency'] = avg_lat
            results[i, j]['dur_err'] = avg_de
            print(f"noise={ns:.3f} th={mf_th:.3f} tp={tp_rate:.3f} fa={avg_false:.2f} lat={avg_lat if not np.isnan(avg_lat) else 'nan'}")
    return noise_list, mf_thresh_list, results

def plot_heatmaps(noise_list, mf_thresh_list, results):
    tp_grid = np.array([[results[i,j]['tp_rate'] for j in range(len(mf_thresh_list))] for i in range(len(noise_list))])
    fa_grid = np.array([[results[i,j]['false_alarm'] for j in range(len(mf_thresh_list))] for i in range(len(noise_list))])

    plt.figure(figsize=(12,5))
    plt.subplot(1,2,1)
    plt.imshow(tp_grid, origin='lower', aspect='auto', extent=[mf_thresh_list[0], mf_thresh_list[-1], noise_list[0], noise_list[-1]])
    plt.colorbar(label='TP Rate')
    plt.xlabel('MF Threshold')
    plt.ylabel('Noise Sigma')
    plt.title('True Positive Rate')

    plt.subplot(1,2,2)
    plt.imshow(fa_grid, origin='lower', aspect='auto', extent=[mf_thresh_list[0], mf_thresh_list[-1], noise_list[0], noise_list[-1]])
    plt.colorbar(label='Avg False Alarms/trial')
    plt.xlabel('MF Threshold')
    plt.ylabel('Noise Sigma')
    plt.title('False Alarms')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    noise_list, mf_thresh_list, results = run_grid(trials=200)
    plot_heatmaps(noise_list, mf_thresh_list, results)
