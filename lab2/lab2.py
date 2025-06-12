import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

import numpy as np


#


# --- Функция системы уравнений ---
def pendulum(
    t,          # время (с)
    y,          # вектор состояния [угол θ (рад), угловая скорость ω (рад/с)]       
    g,          # ускорение свободного падения (м/с^2)
    l,          # длина маятника (м)
    m,          # масса маятника (кг)
    k,          # коэффициент трения
    A,          # амплитуда внешней силы (Н)
    Omega,      # частота внешней силы (рад/с)
   
):
    

    alpha = A / (m * l**2)  # коэффициент внешней силы
    beta = k / (m * l**2)  # коэффициент трения
    gamma = g / l  # коэффициент гравитации

    theta, omega = y
    dtheta_dt = omega
    domega_dt = -beta * omega - gamma * np.sin(theta) + alpha * np.cos(Omega * t)
    
    return [dtheta_dt, domega_dt]


# --- Симуляция движения маятника ---
def simulate_pendulum(
    g = 9.81,     # ускорение свободного падения (м/с^2)
    l = 1.0,      # длина маятника (м)
    m = 1.0,      # масса маятника (кг)
    k = 1,        # коэффициент трения
    A = 0.0,      # амплитуда внешней силы
    Omega = 0,    # частота внешней силы
    pendulum=pendulum,  # функция системы уравнений
    theta0 = np.pi / 4,  # начальный угол (рад)
    omega0 = 0.0,  # начальная угловая скорость (рад/с)
    t_span=(0, 10),  # временной интервал (с)
    n_steps=1000  # количество шагов
):
    
    y0 = [theta0, omega0]
    
    return rk4(lambda t , y : pendulum(t ,y , g , l , m , k , A, Omega), t_span, y0, n_steps)


    y0 = [theta0, omega0]
    t_eval = np.linspace(t_span[0], t_span[1], n_steps + 1)
    def ode(t, y):
        return pendulum(t, y, g, l, m, k, A, Omega)
    
    sol = solve_ivp(ode, t_span, y0, t_eval=t_eval)
    return sol.t, sol.y.T


# --- Визуализация ---
def plot_simulation(t, T, label):
    plt.plot(t, T, label=label)
    plt.xlabel('Время (с)')
    plt.ylabel('Угол θ (рад)')
    plt.grid(True)
    plt.legend(loc='lower right')


def run_free_pendulum_perion_test():
    Ls = [2.4525 , 9.81 , 39.24]
    labels = ['Поведение маятника с дилиной 2.4525 м',
              'Поведение маятника с дилиной 9.81 м',
              'Поведение маятника с дилиной 39.24 м']
    for i, L in enumerate(Ls):

        t, T = simulate_pendulum(l=L, theta0=np.pi / 18, t_span=(0, np.pi * 6), n_steps=10000 , k = 0)
        plt.plot(t, T[ : , 0], label=labels[i])
        plt.xlabel('Время (с)')
        plt.ylabel('Угол θ (рад)')
        plt.grid(True)
        plt.legend(loc='lower right')
  

        pi_ticks = np.arange(0, np.pi * 6, np.pi)
        for x in pi_ticks:
            plt.axvline(x=x, color='gray', linestyle='--')
        plt.show()

def run_friction_test():
    k_s = [ 0.1, 1, 5]

    labels = ['Коэффициент трения 0.1',
              'Коэффициент трения 1',
              'Коэффициент трения 5']
    for i, k in enumerate(k_s):
        t, T = simulate_pendulum(l=1, theta0=np.pi / 18, t_span=(0, np.pi * 6), n_steps=10000, k=k)
        plt.plot(t, T[:, 0], label=labels[i])
        plt.xlabel('Время (с)')
        plt.ylabel('Угол θ (рад)')
        plt.grid(True)
        plt.legend(loc='lower right')

    plt.show()

def run_forced_oscillation_test():
    plt.figure(figsize=(12, 8))

    common_params = dict(
        theta0=np.pi / 6,    # Умеренный начальный угол
        omega0=0.0,          # Без начальной скорости
        Omega=3.13,          # Частота внешней силы, около резонансной (sqrt(g/l) ≈ 3.13)
        t_span=(0, 50),      
        n_steps=3000
    )

    scenarios = [
        {"k": 0.2, "A": 0.0, "label": "Свободные колебания с трением (k=0.2, A=0)"},
        {"k": 0.2, "A": 0.3, "label": "Слабая внешняя сила (A=0.3 < k=0.2)"},
        {"k": 0.2, "A": 0.7, "label": "Внешняя сила сравнима с трением (A≈k)"},
        {"k": 0.2, "A": 1.5, "label": "Сильная внешняя сила (A=1.5 > k)"},
        {"k": 0.05, "A": 1.5, "label": "Малое трение, сильная сила (практически резонанс)"},
        {"k": 0.5, "A": 1.5, "label": "Большое трение, та же сила (A=1.5, k=0.5)"},
    ]

    for scenario in scenarios:
        t, T = simulate_pendulum(
            **common_params,
            k=scenario["k"],
            A=scenario["A"]
        )
        plt.plot(t, T[:, 0], label=scenario["label"])

    plt.xlabel('Время (с)')
    plt.ylabel('Угол θ (рад)')
    plt.title("Вынужденные колебания с трением: сравнительный анализ")
    plt.grid(True)
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    # run_free_pendulum_perion_test()
    # run_friction_test()
    run_forced_oscillation_test()