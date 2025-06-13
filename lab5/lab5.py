import numpy as np
import matplotlib.pyplot as plt
import os
import imageio.v2 as imageio # Added for GIF creation

# --- Основные параметры симуляции (общие для всех экспериментов) ---
L = 2.0       # Длина пространственной области
nx = 201      # Количество точек в пространстве (увеличено для гладкости)
dx = L / (nx - 1) # Шаг по пространству
c = 1         # Скорость переноса
CFL = 0.9     # Число Куранта
dt = CFL * dx / c # Шаг по времени
T = 12.0       # Полное время симуляции
nt = int(T / dt) # Количество временных шагов
nu = c * dt / dx  # Вспомогательное число Куранта

print(dx)
print(dt)


def run_experiment(experiment_name, initial_condition_func):

    output_dir = f"lab5/experiment_{experiment_name}"
    os.makedirs(output_dir, exist_ok=True)

    frames_dir_explicit = os.path.join(output_dir, "frames_explicit")
    os.makedirs(frames_dir_explicit, exist_ok=True)
    frames_dir_implicit = os.path.join(output_dir, "frames_implicit")
    os.makedirs(frames_dir_implicit, exist_ok=True)

    x_space = np.linspace(0, L, nx)
    t_space = np.linspace(0, T, nt)
    u0 = initial_condition_func(x_space, L)
    plt.figure(figsize=(8, 5))
    plt.plot(x_space, u0, 'k-')

    plt.xlabel('Пространство (x)')
    plt.ylabel('Величина (u)')
    plt.grid(True)
    plt.ylim(-1, 2.5)
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
    
    print(f"Running simulation for {experiment_name} and saving slices/frames...")
    period_duration = L / c
    next_save_time_target_s = period_duration
    period_save_counter = 1

    save_frame_interval = max(1, nt // 200)  # Aim for ~200 frames for GIF
    animation_frame_counter = 0
 
    for n in range(1, nt):
        current_time_s = n * dt
        # 1) Явный метод Эйлера с разностями против потока
        un_exp = u_exp.copy()
        for i in range(nx): # Assumes periodic BC due to u_exp[i-1] for i=0
            u_exp[i] = un_exp[i] - nu * (un_exp[i] - un_exp[i-1])
        history_explicit_upwind[n, :] = u_exp

        u_imp = np.linalg.solve(A, u_imp) # u_imp from previous step is used as b for next
        history_implicit_centered[n, :] = u_imp

        if n % save_frame_interval == 0:
            # Explicit method frame
            plt.figure(figsize=(8, 5))
            plt.plot(x_space, u_exp, 'b-', label=f'Explicit Upwind, t={current_time_s:.2f}s')
            plt.xlabel('Пространство (x)')
            plt.ylabel('Величина (u)')
            plt.title(f'Explicit Upwind t={current_time_s:.2f}s - {experiment_name}')
            plt.grid(True)
            plt.ylim(-1, 2.5)
            plt.legend()
            plt.savefig(os.path.join(frames_dir_explicit, f'frame_{animation_frame_counter:04d}.png'))
            plt.close()

            # Implicit method frame
            plt.figure(figsize=(8, 5))
            plt.plot(x_space, u_imp, 'r-', label=f'Implicit Centered, t={current_time_s:.2f}s')
            plt.xlabel('Пространство (x)')
            plt.ylabel('Величина (u)')
            plt.title(f'Implicit Centered t={current_time_s:.2f}s - {experiment_name}')
            plt.grid(True)
            plt.ylim(-1, 2.5)
            plt.legend()
            plt.savefig(os.path.join(frames_dir_implicit, f'frame_{animation_frame_counter:04d}.png'))
            plt.close()
            animation_frame_counter += 1

        if current_time_s >= next_save_time_target_s - dt / 2: # dt/2 for tolerance
            # Сохранение среза для явного метода
            plt.figure(figsize=(8, 5))
            plt.plot(x_space, u_exp, 'b-', label=f'Explicit Upwind, t={current_time_s:.2f}s')
            plt.xlabel('Пространство (x)')
            plt.ylabel('Величина (u)')
            # plt.title(f'Explicit Upwind at t={current_time_s:.2f}s (Period {period_save_counter}) - {experiment_name}')
            plt.grid(True)
            plt.ylim(-1, 2.5)
            plt.legend()
            plt.savefig(os.path.join(output_dir, f'slice_explicit_period_{period_save_counter}.png'))
            plt.close()

            # Сохранение среза для неявного метода
            plt.figure(figsize=(8, 5))
            plt.plot(x_space, u_imp, 'r-', label=f'Implicit Centered, t={current_time_s:.2f}s')
            plt.xlabel('Пространство (x)')
            plt.ylabel('Величина (u)')
            # plt.title(f'Implicit Centered at t={current_time_s:.2f}s (Period {period_save_counter}) - {experiment_name}')
            plt.grid(True)
            plt.ylim(-1, 2.5)
            plt.legend()
            plt.savefig(os.path.join(output_dir, f'slice_implicit_period_{period_save_counter}.png'))
            plt.close()
            
            print(f"  Saved slices for t ~ {current_time_s:.2f}s (target period {period_save_counter}, time {next_save_time_target_s:.2f}s) for {experiment_name}")
            next_save_time_target_s += period_duration
            period_save_counter += 1
            if next_save_time_target_s > T + dt/2: # Stop if we've passed all desired save times
                break
    
    print(f"--- Симуляция для эксперимента '{experiment_name}' завершена. Создание GIF-анимаций... ---")

    # Create GIF for Explicit Method
    images_explicit = []
    frame_files_explicit = sorted([os.path.join(frames_dir_explicit, f) for f in os.listdir(frames_dir_explicit) if f.endswith('.png') and f.startswith('frame_')])
    for filename in frame_files_explicit:
        images_explicit.append(imageio.imread(filename))
    if images_explicit:
        imageio.mimsave(os.path.join(output_dir, 'animation_explicit.gif'), images_explicit, fps=10)
        print(f"  Сохранена анимация: animation_explicit.gif для {experiment_name}")
        # Optional: Clean up individual frames
        # for f in frame_files_explicit: os.remove(f)
        # os.rmdir(frames_dir_explicit)


    # Create GIF for Implicit Method
    images_implicit = []
    frame_files_implicit = sorted([os.path.join(frames_dir_implicit, f) for f in os.listdir(frames_dir_implicit) if f.endswith('.png') and f.startswith('frame_')])
    for filename in frame_files_implicit:
        images_implicit.append(imageio.imread(filename))
    if images_implicit:
        imageio.mimsave(os.path.join(output_dir, 'animation_implicit.gif'), images_implicit, fps=10)
        print(f"  Сохранена анимация: animation_implicit.gif для {experiment_name}")
        # Optional: Clean up individual frames
        # for f in frame_files_implicit: os.remove(f)
        # os.rmdir(frames_dir_implicit)

    print(f"--- Эксперимент '{experiment_name}' полностью завершен (включая GIF). ---\\n")


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
    run_experiment("box", ic_box)
    run_experiment("gaussian", ic_gaussian)
    run_experiment("sine", ic_sine)
    
    print("Все эксперименты завершены.")