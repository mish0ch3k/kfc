import numpy as np

def lorenz(x, y, z, s=10, r=28, b=8/3):
    dx = s * (y - x)
    dy = x * (r - z) - y
    dz = x * y - b * z
    return dx, dy, dz

def simulate(initial_state, time_step=0.01, steps=10000):
    x, y, z = initial_state
    xs, ys, zs = [x], [y], [z]
    for _ in range(steps):
        dx, dy, dz = lorenz(x, y, z)
        x += dx * time_step
        y += dy * time_step
        z += dz * time_step
        xs.append(x)
        ys.append(y)
        zs.append(z)
    return np.array(xs), np.array(ys), np.array(zs)
