import numpy as np
import matplotlib.pyplot as plt
import os

# --- Основные параметры симуляции (общие для всех экспериментов) ---
L = 2.0       # Длина пространственной области
nx = 201      # Количество точек в пространстве (увеличено для гладкости)
dx = L / (nx - 1) # Шаг по пространству
c = 1         # Скорость переноса
CFL = 0.9     # Число Куранта
dt = CFL * dx / c # Шаг по времени
T = 4.0       # Полное время симуляции
nt = int(T / dt) # Количество временных шагов
nu = c * dt / dx  # Вспомогательное число Куранта

print(dx)
print(dt)


def run_experiment(experiment_name, initial_condition_func):

    output_dir = f"lab5/experiment_{experiment_name}"
    os.makedirs(output_dir, exist_ok=True)
    x_space = np.linspace(0, L, nx)
    t_space = np.linspace(0, T, nt)
    u0 = initial_condition_func(x_space, L)
    plt.figure(figsize=(8, 5))
    plt.plot(x_space, u0, 'k-')

    plt.xlabel('Пространство (x)')
    plt.ylabel('Величина (u)')
    plt.grid(True)
    plt.ylim(0, 2.5)
    plt.savefig(os.path.join(output_dir, '01_initial_condition.png'))
    plt.close() 

    history_explicit_upwind = np.zeros((nt, nx))
    history_implicit_centered = np.zeros((nt, nx))

    u_exp = u0.copy()
    u_imp = u0.copy()
    history_explicit_upwind[0, :] = u0
    history_implicit_centered[0, :] = u0

    A = np.zeros((nx, nx))
    nu_half = nu / 2
    A += np.diag(np.ones(nx))  
    A += np.diag(np.ones(nx - 1) * nu_half, k=1)  
    A += np.diag(np.ones(nx - 1) * -nu_half, k=-1) 

    A[0, -1] = -nu_half
    A[-1, 0] = nu_half
    
 
    for n in range(1, nt):
        # 1) Явный метод Эйлера с разностями против потока
        un_exp = u_exp.copy()
        for i in range(nx):
            u_exp[i] = un_exp[i] - nu * (un_exp[i] - un_exp[i-1])
        history_explicit_upwind[n, :] = u_exp

        # 2) Неявный центрально-разностный метод Эйлера
        u_imp = np.linalg.solve(A, u_imp)
        history_implicit_centered[n, :] = u_imp


    print("Сохранение тепловых карт...")
    

    plt.figure(figsize=(8, 6))
    plt.pcolormesh(x_space, t_space, history_explicit_upwind, cmap='inferno', shading='gouraud')

    plt.xlabel('Пространство (x)')
    plt.ylabel('Время (t)')
    plt.colorbar(label='u')
    plt.savefig(os.path.join(output_dir, '02_heatmap_explicit_upwind.png'))
    plt.close()


    plt.figure(figsize=(8, 6))
    plt.pcolormesh(x_space, t_space, history_implicit_centered, cmap='inferno', shading='gouraud')

    plt.xlabel('Пространство (x)')
    plt.ylabel('Время (t)')
    plt.colorbar(label='u')
    plt.savefig(os.path.join(output_dir, '03_heatmap_implicit_centered.png'))
    plt.close()
    
    print(f"--- Эксперимент '{experiment_name}' завершен. ---\n")


def ic_box(x, L):
    """Прямоугольный импульс"""
    u = np.ones_like(x)
    u[(x >= L/4) & (x <= L/2)] = 2.0
    return u

def ic_gaussian(x, L):
    """Гауссов импульс (колокол)"""
    return np.exp(-((x - L/2) / (L/10))**2)

def ic_sine(x, L):
    """Одна полная волна синусоиды"""
    return 1.5 + 0.5 * np.sin(2 * np.pi * x / L)


if __name__ == '__main__':
    # Запускаем три эксперимента один за другим
    run_experiment("box", ic_box)
    run_experiment("gaussian", ic_gaussian)
    run_experiment("sine", ic_sine)
    
    print("Все эксперименты завершены.")