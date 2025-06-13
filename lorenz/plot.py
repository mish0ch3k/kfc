import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from lorenz import simulate

state1 = (1.0, 1.0, 1.0)
state2 = (1.001, 1.0, 1.0)

x1, y1, z1 = simulate(state1)
x2, y2, z2 = simulate(state2)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x1, y1, z1, label="Initial state (1.0, 1.0, 1.0)")
ax.plot(x2, y2, z2, label="Slightly different (1.001, 1.0, 1.0)")
ax.legend()
ax.set_title("Атрактор Лоренца: ефект метелика")
plt.show()
