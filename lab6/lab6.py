import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# --- 1. Настройка параметров симуляции ---
# На основе раздела 2.1, 2.2, 2.3 документа
NUM_PARTICLES = 20000  # Количество частиц, как в полном расчете 
DT = 0.001             # Шаг интегрирования 
T_MAX = 0.4            # Максимальное время моделирования 
PLOT_TIMES = [0.0, 0.1, 0.2, 0.3, 0.4] # Моменты времени для вывода результатов
GRID_SIZE = 500        # Размер сетки для интерполяции 

# --- 2. Определение поля скоростей ---
# Формулы из раздела 2.1 
def u(x, y):
    """Компонента скорости по оси X."""
    return -np.pi * np.sin(2 * np.pi * x) * np.cos(np.pi * y)

def v(x, y):
    """Компонента скорости по оси Y."""
    return 2 * np.pi * np.cos(2 * np.pi * x) * np.sin(np.pi * y)

def velocity_field(points):
    """Возвращает вектор скорости для набора точек."""
    x = points[:, 0]
    y = points[:, 1]
    return np.array([u(x, y), v(x, y)]).T

# --- 3. Реализация метода Рунге-Кутты 4-го порядка ---
# Метод указан в разделе 2.2 
def rk4_step(points, dt, turbulence=False):
    """Один шаг интегрирования методом РК4."""
    
    # Добавление турбулентного компонента, если флаг установлен
    # Модель турбулентности из раздела 2.4 
    def get_velocity(p):
        vel = velocity_field(p)
        if turbulence:
            # Случайные величины ξ_x, ξ_y ~ U[-0.5, 0.5] 
            turb_component = np.random.uniform(-0.5, 0.5, size=vel.shape)
            vel += turb_component
        return vel

    k1 = get_velocity(points)
    k2 = get_velocity(points + 0.5 * dt * k1)
    k3 = get_velocity(points + 0.5 * dt * k2)
    k4 = get_velocity(points + dt * k3)
    
    new_points = points + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    
    return new_points

# --- 4. Визуализация результатов ---
def plot_simulation_state(points, concentrations, time, grid_x, grid_y):
    """Создает и сохраняет изображение с состоянием системы."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    fig.suptitle(f'Момент времени: {time:.2f}', fontsize=16)

    # Левый график: распределение частиц
    ax1.scatter(points[:, 0], points[:, 1], c=concentrations, s=1, cmap='viridis', vmin=-1.5, vmax=1.5)
    ax1.set_title('Распределение частиц')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect('equal', adjustable='box')

    # Правый график: интерполированное поле
    # Метод интерполяции указан в разделе 2.3 
    interpolated_grid = griddata(points, concentrations, (grid_x, grid_y), method='linear')
    im = ax2.imshow(interpolated_grid.T, extent=(0, 1, 0, 1), origin='lower', cmap='viridis', vmin=-1.5, vmax=1.5)
    ax2.set_title('Интерполяция концентрации')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_aspect('equal', adjustable='box')
    
    # Добавление цветовой шкалы
    fig.colorbar(im, ax=ax2, orientation='vertical')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f"simulation_t_{time:.1f}.png")
    plt.show()


def run_simulation(turbulence=False):
    """Основная функция для запуска и визуализации симуляции."""
    # --- Инициализация частиц ---
    # Область [0,1]x[0,1] 
    points = np.random.rand(NUM_PARTICLES, 2) 
    
    # Начальное распределение концентрации C_0(x,y) = arctan((y-0.5)/0.1) 
    y_coords = points[:, 1]
    concentrations = np.arctan((y_coords - 0.5) / 0.1)

    # Сетка для интерполяции
    grid_x, grid_y = np.mgrid[0:1:complex(0, GRID_SIZE), 0:1:complex(0, GRID_SIZE)]

    # --- Основной цикл симуляции ---
    current_time = 0.0
    time_steps = int(T_MAX / DT)
    
    print(f"Запуск симуляции {'с турбулентностью' if turbulence else 'без турбулентности'}...")

    # Сохраняем начальное состояние
    plot_simulation_state(points, concentrations, 0.0, grid_x, grid_y)

    for i in range(1, time_steps + 1):
        points = rk4_step(points, DT, turbulence=turbulence)
        current_time = i * DT
        
        # Проверяем, нужно ли визуализировать текущий шаг
        if any(np.isclose(current_time, p_time) for p_time in PLOT_TIMES[1:]):
            print(f"Визуализация в момент времени t={current_time:.2f}...")
            plot_simulation_state(points, concentrations, current_time, grid_x, grid_y)
    
    print("Симуляция завершена.")


if __name__ == '__main__':
    # Запуск симуляции без турбулентности (основная модель)
    run_simulation(turbulence=False)
    
    # Запуск симуляции с турбулентностью (раздел 2.4)
    # run_simulation(turbulence=True) # Раскомментируйте для запуска