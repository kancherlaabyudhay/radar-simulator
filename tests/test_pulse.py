from src.pulse import generate_rect_pulse

def test_pulse_length():
    fs = 1000
    duration = 0.1
    t, pulse = generate_rect_pulse(fs, duration, 0.02, 0.04)
    assert len(t) == int(fs*duration)
    assert pulse.max() == 1.0
