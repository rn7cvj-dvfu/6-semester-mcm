import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Параметры модели
a = 1.1  # рождаемость жертв
b = 0.4  # интенсивность охоты
c = 0.4  # коэффициент взаимодействия
d = 0.4  # смертность хищников

def lotka_volterra(t, z):
    x, y = z
    dxdt = a * x - b * x * y
    dydt = c * x * y - d * y
    return [dxdt, dydt]

# Начальные условия для трёх экспериментов
initial_conditions = [
    (40, 9),
    (20, 30),
    (80, 5),
]

t_span = (0, 128)  # интервал времени моделирования
t_eval = np.linspace(*t_span, 1000)  # точки для вывода решения

for i, (x0, y0) in enumerate(initial_conditions):
    sol = solve_ivp(lotka_volterra, t_span, [x0, y0], t_eval=t_eval, method='RK45')

    x = sol.y[0]
    y = sol.y[1]
    t = sol.t

    plt.figure(figsize=(12, 7))

    # График численности по времени
    # plt.subplot(1, 2, 1)
    plt.plot(t, x, label='Жертвы (x)')
    plt.plot(t, y, label='Хищники (y)')
    plt.title(f'Эксперимент {i+1}: x0={x0}, y0={y0}')
    plt.xlabel('Время')
    # plt.yscale('log')
    plt.ylabel('Численность')
    
    
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    
    plt.figure(figsize=(12, 7))
    # Фазовый портрет (y от x)
    # plt.subplot(1, 2, 2)
    plt.plot(x, y, color='purple')
    plt.title(f'Фазовая траектория (Эксперимент {i+1})')
    plt.xlabel('Жертвы (x)')
    plt.ylabel('Хищники (y)')
    plt.grid(True)

    plt.tight_layout()
    plt.show()
