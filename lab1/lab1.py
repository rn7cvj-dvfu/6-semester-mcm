import numpy as np
import matplotlib.pyplot as plt

# --- Константы ---
sigma = 5.67e-8  # Постоянная Стефана-Больцмана, Вт/(м²·К⁴)
T_k_0 = 273.13   # 0°C в Кельвинах

# --- Управление терморегулятором ---
def thermostat_control(T, heating, T_min, T_max):
    if heating and T >= T_max:
        return False
    elif not heating and T <= T_min:
        return True
    return heating

# --- Симуляция нагревателя ---
def simulate_heater(
    P=100,            # мощность (Вт)
    m=0.3,            # масса (кг)
    c=500,            # уд. теплоемкость (Дж/кг·К)
    A=0.01,           # площадь теплообмена (м²)
    k=10,             # коэфф. теплообмена (Вт/м²·К)
    T_min_C=70,       # мин. температура терморегулятора (°C)
    T_max_C=100,      # макс. температура терморегулятора (°C)
    T0_C=20,          # начальная температура (°C)
    T_env_C=20,       # температура среды (°C)
    time=2400,        # общее время симуляции (с)
    dt=0.1,           # шаг по времени (с)
    thermostat_control = lambda T, heating, T_min, T_max: True, # функция управления терморегулятором
    eta=lambda T: 0.9 # КПД как функция от температуры
):
    # Перевод в Кельвины
    T_min = T_min_C + T_k_0
    T_max = T_max_C + T_k_0
    T0 = T0_C + T_k_0
    T_env = T_env_C + T_k_0

    n_steps = int(time / dt)
    T = np.zeros(n_steps)
    t = np.linspace(0, time, n_steps)
    T[0] = T0
    heating = True

    for i in range(1, n_steps):
        current_T = T[i - 1]

        # Управление терморегулятором
        heating = thermostat_control(current_T, heating, T_min, T_max)
        thermostat_effect = 1 if heating else 0

        # Энергетические потоки
        q_gen = P * eta(current_T) * dt * thermostat_effect
        q_conv = k * A * (current_T - T_env) * dt
        q_rad = sigma * A * (current_T**4 - T_env**4) * dt

        delta_U = q_gen - q_conv - q_rad
        dT = delta_U / (m * c)
        T[i] = current_T + dT

    return t, T - T_k_0  # Возвращаем температуру в °C

# --- Визуализация ---
def plot_simulation(t, T, label):
    plt.plot(t, T, label=label)
    plt.xlabel('Время (с)')
    plt.ylabel('Температура (°C)')
    plt.grid(True)
    plt.legend(loc='lower right')

# --- Проведение экспериментов ---
def run_experiments():
    plt.figure(figsize=(12, 7))

    # Все параметры одинаковы, кроме T_min_C и T_max_C
    base_params = dict(P=100, m=0.3, A=0.01, k=10)
    t1, T1 = simulate_heater(**base_params, T_min_C=60, T_max_C=80, thermostat_control= lambda current_T, heating, T_min, T_max : True)
    plot_simulation(t1, T1, "P = 100 Вт, m = 0.3 кг, A = 0.01 м², k = 10 Вт/м²·К,")

    base_params = dict(P=100, m=0.6, A=0.01, k=10)
    t2, T2 = simulate_heater(**base_params, T_min_C=70, T_max_C=90)
    plot_simulation(t2, T2, "P = 100 Вт, m = 0.6 кг, A = 0.01 м², k = 10 Вт/м²·К")

    base_params = dict(P=100, m=0.3, A=0.005, k=10)
    t3, T3 = simulate_heater(**base_params, T_min_C=80, T_max_C=100)
    plot_simulation(t3, T3, "P = 100 Вт, m = 0.6 кг, A = 0.005 м², k = 10 Вт/м²·К")

    base_params = dict(P=150, m=0.3, A=0.01, k=10)
    t4, T4 = simulate_heater(**base_params, T_min_C=90, T_max_C=110)
    plot_simulation(t4, T4, "P = 150 Вт, m = 0.6 кг, A = 0.01 м², k = 10 Вт/м²·К")

    base_params = dict(P=100, m=0.3, A=0.01, k=5)
    t5, T5 = simulate_heater(**base_params, T_min_C=100, T_max_C=120)
    plot_simulation(t5, T5, "P = 100 Вт, m = 0.6 кг, A = 0.01 м², k = 5 Вт/м²·К")

    plt.title("Сравнение поведения нагревателя при разных параметрах")
    plt.show()

def run_Tmin_Tmax_experiments():
    plt.figure(figsize=(12, 7))
    base_params = dict(P=100, m=0.3, A=0.01, k=10)
    t1, T1 = simulate_heater(**base_params, T_min_C=60, T_max_C=80 , thermostat_control=thermostat_control )
    plot_simulation(t1, T1, "T_min=60°C, T_max=80°C")
    
    t2, T2 = simulate_heater(**base_params, T_min_C=100, T_max_C=110, thermostat_control=thermostat_control)
    plot_simulation(t2, T2, "T_min=100°C, T_max=110°C")
    t3, T3 = simulate_heater(**base_params, T_min_C=120, T_max_C=125,    thermostat_control=thermostat_control)
    plot_simulation(t3, T3, "T_min=120°C, T_max=125°C")
    t4, T4 = simulate_heater(**base_params, T_min_C=150, T_max_C=170, thermostat_control=thermostat_control)
    plot_simulation(t4, T4, "T_min=150°C, T_max=170°C")
    t5, T5 = simulate_heater(**base_params, T_min_C=250, T_max_C=280 , thermostat_control=thermostat_control)
    plot_simulation(t5, T5, "T_min=250°C, T_max=280")
    plt.title("Влияние T_min и T_max на поведение нагревателя")
    plt.show()

def run_power_experiment():
    plt.figure(figsize=(12, 7))
    base_params = dict(m=0.3, S=0.01, k=10, T_min_C=70, T_max_C=100)
    t1, T1 = simulate_heater(**base_params, P=50)
    plot_simulation(t1, T1, "P=50 Вт")
    t2, T2 = simulate_heater(**base_params, P=100)
    plot_simulation(t2, T2, "P=100 Вт")
    t3, T3 = simulate_heater(**base_params, P=150)
    plot_simulation(t3, T3, "P=150 Вт")
    plt.title("Влияние мощности на поведение нагревателя")
    plt.show()

def run_k_experiment():
    plt.figure(figsize=(12, 7))
    base_params = dict(P=100, m=0.3, S=0.01, T_min_C=70, T_max_C=100)
    t1, T1 = simulate_heater(**base_params, k=5)
    plot_simulation(t1, T1, "k=5 Вт/м²·К")
    t2, T2 = simulate_heater(**base_params, k=10)
    plot_simulation(t2, T2, "k=10 Вт/м²·К")
    t3, T3 = simulate_heater(**base_params, k=20)
    plot_simulation(t3, T3, "k=20 Вт/м²·К")
    plt.title("Влияние коэффициента теплообмена на поведение нагревателя")
    plt.show()

def run_eta_experiment():
    plt.figure(figsize=(12, 7))
    base_params = dict(P=300, m=0.3, S=0.01, k=10, T_min_C=70, T_max_C=100 , time=50 )
    t1, T1 = simulate_heater(**base_params, eta=lambda T: 0.2 +  min(0.8 , 0.8 * (T - T_k_0) / 40))
    plot_simulation(t1, T1, "η=0.2 + min(0.8, 0.8·(T-273)/40)")
    t2, T2 = simulate_heater(**base_params, eta=lambda T: 0.2 + 0.8 * np.sin((T-T_k_0) / 60 * np.pi))
    plot_simulation(t2, T2, "η=0.2 + 0.8·sin((T-273)/60·π)")
    # t3, T3 = simulate_heater(**base_params, eta=lambda T: 0.9 - 0.2 * np.exp(-(T-273)/200))
    # plot_simulation(t3, T3, "η=0.9-0.2·exp(-(T-273)/200)")
    plt.title("Влияние  КПД на поведение нагревателя")
    plt.show()

# --- Точка входа ---
if __name__ == "__main__":
    run_experiments()
    # run_Tmin_Tmax_experiments()
    # run_power_experiment()
    # run_k_experiment()
    # run_eta_experiment()
