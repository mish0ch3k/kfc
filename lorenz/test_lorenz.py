from lorenz import simulate
import numpy as np

def test_chaos_sensitivity():
    x1, y1, z1 = simulate((1.0, 1.0, 1.0), steps=5000)
    x2, y2, z2 = simulate((1.001, 1.0, 1.0), steps=5000)
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2)
    assert distance[-1] > 10, "Системи повинні значно розійтись через хаотичну чутливість"
