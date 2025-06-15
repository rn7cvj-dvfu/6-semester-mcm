import numpy as np
import matplotlib.pyplot as plt
import os

# Параметры модели
R = 5.0      # радиус вращающегося диска
dt = 0.01    # шаг по времени
T = 20.0     # общее время моделирования
N = int(T / dt)

# Создаем папку для графиков, если ее нет
os.makedirs("lab4/plots_coriolis_only", exist_ok=True)

color = "#F4A300"

def draw_experiment_plot(x, y, omega, exp_num):
    """
    Функция для отрисовки и сохранения графика траектории.
    """
    fig, ax = plt.subplots(figsize=(6, 6))

    # Рисуем границу диска
    circle = plt.Circle((0, 0), R, color="gray", linestyle="--", fill=False, linewidth=1)
    ax.add_artist(circle)

    # Рисуем траекторию движения
    ax.plot(x, y, color=color, linewidth=2, label=f"$\\omega={omega:.1f}$ рад/с")

    # Настройки графика
    ax.set_xlim(-R - 1, R + 1)
    ax.set_ylim(-R - 1, R + 1)
    ax.set_aspect('equal', adjustable='box') 

    ax.set_xlabel("x, м")
    ax.set_ylabel("y, м")
    ax.set_title(f"Эксперимент {exp_num} (только сила Кориолиса)")
    ax.grid(True)
    ax.legend(loc="upper right")
  
    # Сохраняем график в файл
    plt.savefig(f"lab4/plots_coriolis_only/experiment_{exp_num}.png", dpi=300,  bbox_inches='tight')
    plt.close()

def simulate_motion(
    omega, # угловая скорость вращения диска 
    x0,    # начальная координата x
    y0,    # начальная координата y
    vx0,   # начальная скорость по x
    vy0,   # начальная скорость по y
    exp_num # номер эксперимента (для сохранения графика)
):
    """
    Основная функция моделирования движения.
    """
    # Массивы для хранения координат и скоростей
    x = np.zeros(N)
    y = np.zeros(N)
    vx = np.zeros(N)
    vy = np.zeros(N)

    # Начальные условия
    x[0], y[0] = x0, y0
    vx[0], vy[0] = vx0, vy0

    # Цикл моделирования
    for i in range(N - 1):
        x_i, y_i = x[i], y[i]
        vx_i, vy_i = vx[i], vy[i]

        # --- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ ---
        # Ускорение теперь учитывает ТОЛЬКО силу Кориолиса.
        # Мы убрали слагаемые omega**2 * x_i и omega**2 * y_i
        ax = 2 * omega * vy_i
        ay = -2 * omega * vx_i

        # Обновляем скорость и положение по методу Эйлера
        vx[i + 1] = vx_i + ax * dt
        vy[i + 1] = vy_i + ay * dt
        x[i + 1] = x_i + vx[i + 1] * dt
        y[i + 1] = y_i + vy[i + 1] * dt

        # Проверка выхода за границу диска
        if x[i + 1]**2 + y[i + 1]**2 > R**2:
            x = x[:i + 2]
            y = y[:i + 2]
            break

    # Отрисовка результата
    draw_experiment_plot(x, y, omega, exp_num)

# --- Запуск экспериментов ---
simulate_motion(omega=1.0, x0=1.0, y0=0.0, vx0=0.0, vy0=2.0, exp_num=1)
simulate_motion(omega=2.0, x0=0.0, y0=1.0, vx0=2.0, vy0=0.0, exp_num=2)
simulate_motion(omega=3.0, x0=2.0, y0=0.0, vx0=0.0, vy0=1.5, exp_num=3)
simulate_motion(omega=1.5, x0=1.0, y0=1.0, vx0=1.0, vy0=-1.0, exp_num=4)

print("Моделирование завершено! Графики сохранены в папке 'lab4/plots_coriolis_only'.")