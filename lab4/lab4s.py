import numpy as np
import matplotlib.pyplot as plt
import os

# Определяем базовую директорию, где лежит скрипт. Файлы будут сохраняться сюда.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =============================================================================
# Блок с функциями модели и решателя (остается без изменений)
# =============================================================================

def model_rhs(s, t, omega):
    """Определяет правую часть системы ОДУ."""
    x, y, u, v = s
    dxdt = u
    dydt = v
    dudt = 2 * omega * v
    dvdt = -2 * omega * u
    return np.array([dxdt, dydt, dudt, dvdt])

def runge_kutta_4_solver(f, s0, t_span, dt, **f_args):
    """Решает систему ОДУ методом Рунге-Кутты 4-го порядка."""
    t_start, t_end = t_span
    t_values = np.arange(t_start, t_end + dt, dt)
    n_steps = len(t_values)
    solution_history = np.zeros((n_steps, len(s0)))
    solution_history[0] = s0
    
    for n in range(n_steps - 1):
        s_n = solution_history[n]
        t_n = t_values[n]
        k1 = f(s_n, t_n, **f_args)
        k2 = f(s_n + 0.5 * dt * k1, t_n + 0.5 * dt, **f_args)
        k3 = f(s_n + 0.5 * dt * k2, t_n + 0.5 * dt, **f_args)
        k4 = f(s_n + dt * k3, t_n + dt, **f_args)
        s_n_plus_1 = s_n + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        solution_history[n+1] = s_n_plus_1
        
    return t_values, solution_history

# =============================================================================
# НОВАЯ ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ ОТРИСОВКИ СТРЕЛОК
# =============================================================================
def add_arrows_to_plot(ax, x, y, u, v):
    """
    Добавляет на график стрелки, указывающие направление движения.
    """
    # Рисуем стрелку каждые N шагов, чтобы не загромождать график
    arrow_skip = 250
    arrow_indices = np.arange(arrow_skip, len(x) - 1, arrow_skip)
    
    # Если на траектории есть место для стрелок
    if len(arrow_indices) > 0:
        ax.quiver(
            x[arrow_indices], y[arrow_indices], 
            u[arrow_indices], v[arrow_indices],
            color='black',       # Контрастный черный цвет
            angles='xy',         # Направление стрелок соответствует данным
            scale_units='xy',    # Масштаб стрелок соответствует осям
            scale=12,            # Уменьшили scale, чтобы стрелки стали ДЛИННЕЕ
            headwidth=5,         # Увеличили ширину наконечника
            headlength=7,        # Увеличили длину наконечника
            width=0.004,         # Толщина линии стрелки
            zorder=2             # Слой отрисовки (поверх линии, под точками)
        )

# =============================================================================
# Блок проведения и визуализации экспериментов (с изменениями)
# =============================================================================

def run_experiments_and_save():
    """Запускает эксперименты и сохраняет результаты в файлы."""
    
    T = 20.0
    omega_base = 2 * np.pi / T
    t_span = (0.0, 40.0)
    dt = 0.01

    # --- Эксперимент 1: Влияние начальной скорости ---
    fig1, axs1 = plt.subplots(2, 2, figsize=(12, 12))
    fig1.suptitle('Эксперимент 1: Влияние начальной скорости', fontsize=16)
    
    velocity_cases = [
        {'u0': 1.0, 'v0': 0.0, 'title': 'Базовый случай (u0=1, v0=0)'},
        {'u0': 2.0, 'v0': 0.0, 'title': 'Увеличенная скорость (u0=2, v0=0)'},
        {'u0': 1.0, 'v0': 1.0, 'title': 'Другое направление (u0=1, v0=1)'},
        {'u0': 0.0, 'v0': 0.0, 'title': 'Нулевая скорость (u0=0, v0=0)'}
    ]
    
    for ax, case in zip(axs1.flat, velocity_cases):
        s0 = np.array([0.0, 0.0, case['u0'], case['v0']])
        t, sol = runge_kutta_4_solver(model_rhs, s0, t_span, dt, omega=omega_base)
        x, y, u, v = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
        
        ax.plot(x, y, color='blue', zorder=1)
        ax.plot(s0[0], s0[1], 'go', markersize=8, label='Старт', zorder=3)
        add_arrows_to_plot(ax, x, y, u, v) # Вызов новой функции
        
        ax.set_title(case['title'])
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_aspect('equal', 'box')
        ax.grid(True)
        ax.legend()
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    filename1 = os.path.join(BASE_DIR, "experiment_1_velocity.png")
    fig1.savefig(filename1, dpi=300, bbox_inches='tight')
    print(f"График 'Эксперимент 1' сохранен в файл: {filename1}")
    plt.close(fig1)

    # --- Эксперимент 2: Влияние начального положения ---
    fig2, ax2 = plt.subplots(figsize=(8, 8))
    fig2.suptitle('Эксперимент 2: Влияние начального положения', fontsize=16)

    position_cases = [
        {'x0': 0.0, 'y0': 0.0, 'label': 'Старт из центра (0,0)'},
        {'x0': 2.0, 'y0': 1.0, 'label': 'Старт из точки (2,1)'}
    ]
    
    colors = ['blue', 'green']
    for color, case in zip(colors, position_cases):
        s0 = np.array([case['x0'], case['y0'], 1.0, 0.0])
        t, sol = runge_kutta_4_solver(model_rhs, s0, t_span, dt, omega=omega_base)
        x, y, u, v = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
        
        ax2.plot(x, y, color=color, label=case['label'], zorder=1)
        ax2.plot(s0[0], s0[1], 'o', color=color, markersize=8, zorder=3)
        add_arrows_to_plot(ax2, x, y, u, v) # Вызов новой функции

    ax2.set_title('Сравнение траекторий при разном старте')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_aspect('equal', 'box')
    ax2.grid(True)
    ax2.legend()
    
    filename2 = os.path.join(BASE_DIR, "experiment_2_position.png")
    fig2.savefig(filename2, dpi=300, bbox_inches='tight')
    print(f"График 'Эксперимент 2' сохранен в файл: {filename2}")
    plt.close(fig2)

    # --- Эксперимент 3: Влияние угловой скорости (ω) ---
    fig3, ax3 = plt.subplots(figsize=(8, 8))
    fig3.suptitle('Эксперимент 3: Влияние угловой скорости ω', fontsize=16)
    
    omega_cases = [
        {'omega': omega_base, 'label': f'Стандартная ω ({omega_base:.2f} рад/с)'},
        {'omega': omega_base * 2, 'label': f'Удвоенная ω ({omega_base*2:.2f} рад/с)'}
    ]
    
    s0 = np.array([0.0, 0.0, 1.0, 0.0])
    colors = ['blue', 'red']
    for color, case in zip(colors, omega_cases):
        t, sol = runge_kutta_4_solver(model_rhs, s0, t_span, dt, omega=case['omega'])
        x, y, u, v = sol[:, 0], sol[:, 1], sol[:, 2], sol[:, 3]
        
        ax3.plot(x, y, color=color, label=case['label'], zorder=1)
        add_arrows_to_plot(ax3, x, y, u, v) # Вызов новой функции
        
    ax3.plot(s0[0], s0[1], 'go', markersize=8, label='Старт (общий)', zorder=3)
    ax3.set_title('Сравнение траекторий при разной скорости вращения')
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_aspect('equal', 'box')
    ax3.grid(True)
    ax3.legend()
    
    filename3 = os.path.join(BASE_DIR, "experiment_3_omega.png")
    fig3.savefig(filename3, dpi=300, bbox_inches='tight')
    print(f"График 'Эксперимент 3' сохранен в файл: {filename3}")
    plt.close(fig3)

# --- Запуск всех экспериментов ---
if __name__ == "__main__":
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    run_experiments_and_save()
    print("\nВсе эксперименты завершены, графики со стрелками сохранены.")