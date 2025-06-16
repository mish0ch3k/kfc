import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

SUSCEPTIBLE, INFECTED, RECOVERED = 0, 1, 2

# === КОНФІГУРАЦІЯ КОРИСТУВАЧЕМ ===
P_infect = float(input("Ймовірність зараження (наприклад, 0.3): "))
T_recover = int(input("Час до одужання (ціле число, наприклад, 10): "))
grid_size = int(input("Розмір сітки (наприклад, 50): "))
steps = 100

# === ІНІЦІАЛІЗАЦІЯ ===
state = np.zeros((grid_size, grid_size), dtype=int)
time_infected = np.zeros_like(state)

center = grid_size // 2
state[center, center] = INFECTED

# === ОНОВЛЕННЯ ===
def update(frame):
    global state, time_infected
    new_state = state.copy()
    new_time = time_infected.copy()

    for i in range(grid_size):
        for j in range(grid_size):
            if state[i, j] == SUSCEPTIBLE:
                neighbors = state[max(i - 1, 0):min(i + 2, grid_size),
                                  max(j - 1, 0):min(j + 2, grid_size)]
                if np.any(neighbors == INFECTED) and np.random.rand() < P_infect:
                    new_state[i, j] = INFECTED
            elif state[i, j] == INFECTED:
                new_time[i, j] += 1
                if new_time[i, j] >= T_recover:
                    new_state[i, j] = RECOVERED

    state[:] = new_state
    time_infected[:] = new_time
    mat.set_data(state)
    return [mat]

# === ВІЗУАЛІЗАЦІЯ ===
fig, ax = plt.subplots()
plt.title("SIR-модель епідемії")
mat = ax.matshow(state, cmap=plt.get_cmap('viridis', 3), vmin=0, vmax=2)
plt.colorbar(mat, ticks=[0, 1, 2], label="Стан (0=S, 1=I, 2=R)")
ax.set_xticks([]); ax.set_yticks([])

ani = animation.FuncAnimation(fig, update, frames=steps, interval=150, repeat=False)
globals()['_anim_ref'] = ani  # захист від GC
plt.show()
