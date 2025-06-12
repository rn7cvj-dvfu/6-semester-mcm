import numpy as np
import matplotlib.pyplot as plt
import os

# Параметры модели
R = 5.0      # радиус вращающегося диска
dt = 0.01    # шаг по времени
T = 20.0     # общее время моделирования
N = int(T / dt)

os.makedirs("lab4/plots", exist_ok=True)

color = "#F4A300"

def draw_experiment_plot(x, y, omega, exp_num,):
    fig, ax = plt.subplots(figsize=(6, 6))

    circle = plt.Circle((0, 0), R, color="gray", linestyle="--", fill=False, linewidth=1)
    ax.add_artist(circle)

    ax.plot(x, y, color=color, linewidth=2, label=f"$\\omega={omega:.1f}$ рад/с")

    ax.set_xlim(-R - 1, R + 1)
    ax.set_ylim(-R - 1, R + 1)
    ax.set_aspect('equal', adjustable='box') 

    ax.set_xlabel("x, м")
    ax.set_ylabel("y, м")
    ax.set_title(f"Эксперимент {exp_num}")
    ax.grid(True)
    ax.legend(loc="upper right")
  
    plt.savefig(f"lab4/plots/experiment_{exp_num}.png", dpi=300,  bbox_inches='tight')
    plt.close()

def simulate_motion(
    omega, # угловая скорость вращения диска 
    x0,  # начальная координата x
    y0,  # начальная координата y
    vx0,  # начальная скорость по x
    vy0,  # начальная скорость по y
    exp_num # номер эксперимента (для сохранения графика)
):
    x = np.zeros(N)
    y = np.zeros(N)
    vx = np.zeros(N)
    vy = np.zeros(N)

    x[0], y[0] = x0, y0
    vx[0], vy[0] = vx0, vy0

    for i in range(N - 1):
        x_i, y_i = x[i], y[i]
        vx_i, vy_i = vx[i], vy[i]

        ax = 2 * omega * vy_i + omega**2 * x_i
        ay = -2 * omega * vx_i + omega**2 * y_i

        vx[i + 1] = vx_i + ax * dt
        vy[i + 1] = vy_i + ay * dt
        x[i + 1] = x_i + vx[i + 1] * dt
        y[i + 1] = y_i + vy[i + 1] * dt

        # Проверка выхода за границу диска
        if x[i + 1]**2 + y[i + 1]**2 > R**2:
            x = x[:i + 2]
            y = y[:i + 2]
            break

    draw_experiment_plot(x, y, omega, exp_num)

simulate_motion(omega=1.0, x0=1.0, y0=0.0, vx0=0.0, vy0=2.0, exp_num=1)
simulate_motion(omega=2.0, x0=0.0, y0=1.0, vx0=2.0, vy0=0.0, exp_num=2)
simulate_motion(omega=3.0, x0=2.0, y0=0.0, vx0=0.0, vy0=1.5, exp_num=3)
simulate_motion(omega=1.5, x0=1.0, y0=1.0, vx0=1.0, vy0=-1.0, exp_num=4)

