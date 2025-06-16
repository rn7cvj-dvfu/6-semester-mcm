import numpy as np
import matplotlib.pyplot as plt
import os

# =============================================================================
# 1. ОБЩИЕ ПАРАМЕТРЫ И ФУНКЦИИ
# =============================================================================
T_MAX = 0.4
COMPARE_TIMES = [0.1, 0.2, 0.3, 0.4]

NX, NY = 150, 150
NUM_PARTICLES = 30000


def u(x, y):
    return -np.pi * np.sin(2 * np.pi * x) * np.cos(np.pi * y)

def v(x, y):
    return 2 * np.pi * np.cos(2 * np.pi * x) * np.sin(np.pi * y)

def c_0(x, y):
    return np.sin( (x * y - 0.5) / 0.1)

# =============================================================================
# 2. РЕАЛИЗАЦИЯ МЕТОДА ЧАСТИЦ (ЛАГРАНЖЕВ ПОДХОД)
# =============================================================================
def run_particle_method(target_times , c_0 = c_0):
    print("Запуск симуляции: Метод частиц...")
    from scipy.interpolate import griddata

    points = np.random.rand(NUM_PARTICLES, 2)
    concentrations = c_0(points[:, 0], points[:, 1])
    
    dt = 0.001
    time = 0.0
    results = {}
    
    def velocity_field(p):
        return np.array([u(p[:, 0], p[:, 1]), v(p[:, 0], p[:, 1])]).T

    max_time_to_run = max(target_times)
    times_to_save = sorted(target_times)
    
    # ИСПРАВЛЕНИЕ: Добавляем небольшой буфер (dt/2) к условию цикла
    while time <= max_time_to_run + dt / 2:
        if times_to_save and time >= times_to_save[0]:
            current_save_time = times_to_save.pop(0)
            print(f"  Метод частиц: сохраняем срез на t={current_save_time:.1f}...")
            grid_x, grid_y = np.mgrid[0:1:complex(0, NX), 0:1:complex(0, NY)]
            interpolated_grid = griddata(points, concentrations, (grid_x, grid_y), method='linear')
            results[current_save_time] = interpolated_grid
        
        k1 = velocity_field(points)
        k2 = velocity_field(points + 0.5 * dt * k1)
        k3 = velocity_field(points + 0.5 * dt * k2)
        k4 = velocity_field(points + dt * k3)
        points += (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        time += dt

    if times_to_save:

        save_time = times_to_save.pop(0)

        print(f"  Метод частиц: сохраняем срез на t={save_time:.1f}...")
        grid_x, grid_y = np.mgrid[0:1:complex(0, NX), 0:1:complex(0, NY)]
        interpolated_grid = griddata(points, concentrations, (grid_x, grid_y), method='linear')
        results[save_time] = interpolated_grid

    print("Метод частиц: симуляция завершена.")
    return results

# =============================================================================
# 3. РЕАЛИЗАЦИЯ КОНЕЧНО-РАЗНОСТНОГО МЕТОДА (ЭЙЛЕРОВ ПОДХОД)
# =============================================================================
def run_finite_difference_method(target_times, initial_C, U_grid, V_grid):
    print("Запуск симуляции: Конечно-разностный метод...")
    C = initial_C.copy()
    dx = 1.0 / (NX - 1)
    dy = 1.0 / (NY - 1)

    u_max, v_max = np.max(np.abs(U_grid)), np.max(np.abs(V_grid))
    dt = 0.5 / (u_max / dx + v_max / dy)
    
    time = 0.0
    results = {}
    times_to_save = sorted(target_times)
    max_time_to_run = max(target_times)
    
    while time <= max_time_to_run + dt / 2:
        if times_to_save and time >= times_to_save[0]:
            current_save_time = times_to_save.pop(0)
            print(f"  К-Р метод: сохраняем срез на t={current_save_time:.1f}...")
            results[current_save_time] = C.copy()

        C_old = C.copy()
        for i in range(1, NX - 1):
            for j in range(1, NY - 1):
                if U_grid[j, i] >= 0:
                    dCdx = (C_old[j, i] - C_old[j, i - 1]) / dx
                else:
                    dCdx = (C_old[j, i + 1] - C_old[j, i]) / dx
                if V_grid[j, i] >= 0:
                    dCdy = (C_old[j, i] - C_old[j - 1, i]) / dy
                else:
                    dCdy = (C_old[j + 1, i] - C_old[j, i]) / dy
                C[j, i] = C_old[j, i] - dt * (U_grid[j, i] * dCdx + V_grid[j, i] * dCdy)
        time += dt

    if times_to_save:
        save_time = times_to_save.pop(0)
        print(f"  К-Р метод: сохраняем срез на t={save_time:.1f}...")
        results[save_time] = C.copy()
    
        
    print("Конечно-разностный метод: симуляция завершена.")
    return results

# =============================================================================
# 4. ФУНКЦИЯ ДЛЯ СОХРАНЕНИЯ ОДИНОЧНОГО ГРАФИКА
# =============================================================================
def save_single_plot(data, title, filename):
    """Создает, настраивает и сохраняет один график."""
    fig, ax = plt.subplots(figsize=(7, 6))
    
    vmin, vmax = -1.5, 1.5
    cmap = 'inferno'
    
    im = ax.imshow(data.T, extent=(0, 1, 0, 1), origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    
    fig.colorbar(im, ax=ax, shrink=0.85)
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close(fig) #
    print(f"Сохранено: {filename}")

# =============================================================================
# 5. ЗАПУСК И ВИЗУАЛИЗАЦИЯ
# =============================================================================
if __name__ == '__main__':
    x = np.linspace(0, 1, NX)
    y = np.linspace(0, 1, NY)
    X, Y = np.meshgrid(x, y)
    C_initial = c_0(X , Y)
    U_grid = u(X, Y)
    V_grid = v(X, Y)

    # --- Запуск симуляций ---
    particle_results = run_particle_method(COMPARE_TIMES)
    fdm_results = run_finite_difference_method(COMPARE_TIMES, C_initial, U_grid, V_grid)

    os.makedirs('lab6/comparison_results', exist_ok=True)

    print("\nСохранение начального состояния...")
    save_single_plot(C_initial.T, 'Начальное состояние (t=0.0)', 'lab6/comparison_results/initial_state.png')

    
    print("\nСохранение результатов по временным срезам...")
    for t in COMPARE_TIMES:
        p_data = particle_results[t]
        p_title = f'Метод частиц (t={t:.1f})'
        p_filename = f'lab6/comparison_results/particle_method_t_{t:.1f}.png'
        save_single_plot(p_data, p_title, p_filename)
        
        fdm_data = fdm_results[t]
        fdm_title = f'Конечно-разностный метод (t={t:.1f})'
        fdm_filename = f'lab6/comparison_results/fdm_method_t_{t:.1f}.png'
        save_single_plot(fdm_data.T, fdm_title, fdm_filename)

    print("\nВсе файлы успешно созданы.")