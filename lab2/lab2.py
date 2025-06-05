import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

import numpy as np


# --- Метод Рунге-Кутты 4-ого порядка ---
def rk4(f, t_span, y0, n_steps):
    t0, t_end = t_span
    h = (t_end - t0) / n_steps
    t = np.linspace(t0, t_end, n_steps + 1)
    y = np.zeros((n_steps + 1, len(y0)))
    y[0] = y0

    for i in range(n_steps):
        k1 = np.array(f(t[i], y[i]))
        k2 = np.array(f(t[i] + h/2, y[i] + h/2 * k1))
        k3 = np.array(f(t[i] + h/2, y[i] + h/2 * k2))
        k4 = np.array(f(t[i] + h, y[i] + h * k3))
        y[i+1] = y[i] + h / 6 * (k1 + 2*k2 + 2*k3 + k4)

    return t, y




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
    theta, omega = y
    dtheta_dt = omega
    domega_dt = -(k / (m * l**2)) * omega - (g / l) * np.sin(theta) + (A / (m * l**2)) * np.cos(Omega * t)
    
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

        t, T = simulate_pendulum(l=L, theta0=np.pi / 2, t_span=(0, np.pi * 6), n_steps=10000 , k = 0)
        plt.plot(t, T[ : , 0], label=labels[i])
        plt.xlabel('Время (с)')
        plt.ylabel('Угол θ (рад)')
        plt.grid(True)
        plt.legend(loc='lower right')
  

        pi_ticks = np.arange(0, np.pi * 6, np.pi)
        for x in pi_ticks:
            plt.axvline(x=x, color='gray', linestyle='--')
        plt.show()



if __name__ == "__main__":
    run_free_pendulum_perion_test()
