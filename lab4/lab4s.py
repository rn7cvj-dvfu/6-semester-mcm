import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import matplotlib.ticker as mticker

# --- Constants ---
T_PERIOD = 10.0
OMEGA_POS = 2 * np.pi / T_PERIOD
T_START = 0.0
T_END_DEFAULT_FOR_TRAJECTORY_VIEW = 15.0
RTOL_VAL = 1e-7
ATOL_VAL = 1e-10

# --- ODE System Definition ---
def ode_system(t, Y, omega_val):
    """
    Defines the system of ordinary differential equations.
    Y = [u, v, x, y] where u, v are velocity components and x, y are position components.
    """
    u, v, x, y = Y
    dudt = 2 * omega_val * v
    dvdt = -2 * omega_val * u
    dxdt = u
    dydt = v
    return [dudt, dvdt, dxdt, dydt]

# --- ODE Solver Function ---
def solve_ode_for_trajectory(omega, x0, y0, u0, v0, t_end_fixed=None):
    """
    Solves the ODE system for a given set of initial conditions and omega.
    Automatically determines the simulation end time if not fixed.
    """
    y0_init = [u0, v0, x0, y0]
    initial_speed_sq = u0 ** 2 + v0 ** 2

    current_t_end = t_end_fixed
    if t_end_fixed is None:
        # Calculate simulation end time based on theoretical revolution period for better visualization
        if initial_speed_sq > 1e-12 and abs(omega) > 1e-9:
            # R = |v0| / |2*omega|
            # Circumference = 2 * pi * R
            # Time for one revolution = Circumference / |v0| = (2 * pi * |v0| / |2*omega|) / |v0| = pi / |omega|
            time_one_particle_revolution = np.pi / abs(omega)
            current_t_end = time_one_particle_revolution * 1.5 # Simulate 1.5 revolutions for clear visualization
        elif initial_speed_sq < 1e-12: # Particle is stationary
            current_t_end = T_PERIOD * 0.05 # Small time for stationary case
        else:
            current_t_end = T_END_DEFAULT_FOR_TRAJECTORY_VIEW # Fallback for edge cases

    num_points = 300
    if initial_speed_sq < 1e-12:
        num_points = 5 # Fewer points for stationary particle

    t_eval = np.linspace(T_START, current_t_end, num_points)
    sol = solve_ivp(ode_system, [T_START, current_t_end], y0_init, args=(omega,),
                    dense_output=True, t_eval=t_eval, method='RK45',
                    rtol=RTOL_VAL, atol=ATOL_VAL)
    
    return sol.t, sol.y[0], sol.y[1], sol.y[2], sol.y[3], initial_speed_sq

# --- Function to Add Trajectory Arrows ---
def add_trajectory_arrows(ax, x_traj, y_traj, color, num_arrows=5):
    """
    Adds directional arrows to a trajectory plot.
    """
    if len(x_traj) <= 1 or num_arrows <= 0 or (np.allclose(x_traj, x_traj[0]) and np.allclose(y_traj, y_traj[0])):
        return

    # Select indices for arrows evenly spaced along the trajectory
    arrow_indices = np.linspace(0, len(x_traj) - 2, num_arrows, dtype=int)
    head_w, head_l = 0.06, 0.1 # Arrow head width and length

    for idx in arrow_indices:
        x_start, y_start = x_traj[idx], y_traj[idx]
        dx, dy = x_traj[idx + 1] - x_start, y_traj[idx + 1] - y_start
        # Only draw arrow if there's significant movement to avoid division by zero for stationary points
        if np.sqrt(dx ** 2 + dy ** 2) > 1e-5:
            ax.arrow(x_start, y_start, dx, dy, head_width=head_w, head_length=head_l,
                     fc=color, ec=color, length_includes_head=True, alpha=0.7)

# --- Global variables to store data for E(t) plot ---
t_for_E, u_for_E, v_for_E, initial_speed_sq_for_E = None, None, None, None

# --- Experiment 1: Influence of initial velocity ---
fig1, ax1 = plt.subplots(figsize=(8, 8))
ax1.set_title(f'Рис. 1: Траектории y(x) для различных начальных скоростей (ω≈{OMEGA_POS:.3f} рад/с)')
ax1.set_xlabel('x, м')
ax1.set_ylabel('y, м')
ax1.grid(True)
ax1.axis('equal')

experiments_e1 = [
    {"x0": 0, "y0": 0, "u0": 1.0, "v0": 0.0, "clr": "blue", "lbl": "E1.1 (u0=1, v0=0)"},
    {"x0": 0, "y0": 0, "u0": 0.0, "v0": 1.5, "clr": "orangered", "lbl": "E1.2 (u0=0, v0=1.5)"},
    {"x0": 0, "y0": 0, "u0": 0.7, "v0": 0.7, "clr": "green", "lbl": "E1.3 (u0=0.7, v0=0.7)"},
]

for i, exp in enumerate(experiments_e1):
    t_end_current = None
    if i == 0: # For E1.1, fixing time for E(t) plot coherence
        t_end_current = 7.8 
    t, u, v, x_sol, y_sol, speed_sq = solve_ode_for_trajectory(
        OMEGA_POS, exp["x0"], exp["y0"], exp["u0"], exp["v0"], t_end_fixed=t_end_current
    )
    ax1.plot(x_sol, y_sol, label=exp["lbl"], linewidth=2, color=exp["clr"])
    ax1.plot(exp["x0"], exp["y0"], 'o', color=exp["clr"], markersize=7, markeredgecolor='black', zorder=5) # Start point
    add_trajectory_arrows(ax1, x_sol, y_sol, exp["clr"])

    # Plot theoretical center of the circle
    if speed_sq > 1e-12 and abs(OMEGA_POS) > 1e-9:
        xc_th = exp["x0"] + exp["v0"] / (2 * OMEGA_POS)
        yc_th = exp["y0"] - exp["u0"] / (2 * OMEGA_POS)
        ax1.plot(xc_th, yc_th, 'x', color=exp["clr"], markersize=8, mew=1.5, zorder=5) # Center point
    
    if i == 0: # Store data for E(t) plot from E1.1
        t_for_E, u_for_E, v_for_E, initial_speed_sq_for_E = t, u, v, speed_sq

ax1.legend()
fig1.tight_layout()
fig1.savefig('Рисунок_1.png', dpi=300) # Save the figure

# --- Experiment 2: Special initial conditions ---
fig2, ax2 = plt.subplots(figsize=(8, 8))
ax2.set_title(f'Рис. 2: Траектории для особых начальных условий (ω≈{OMEGA_POS:.3f} рад/с)')
ax2.set_xlabel('x, м')
ax2.set_ylabel('y, м')
ax2.grid(True)
ax2.axis('equal')

# E2.1: Zero initial velocity
t, u, v, x_sol, y_sol, speed_sq = solve_ode_for_trajectory(OMEGA_POS, 0, 0, 0, 0)
# For a stationary point, plot just the single point
ax2.plot(x_sol[0], y_sol[0], 'o', color='purple', markersize=8, markeredgecolor='black', label='E2.1 (u0=0, v0=0)', zorder=5)

# E2.2: Non-zero initial position and velocity
x0, y0, u0, v0 = 1.0, 0.5, 0.5, -0.5
t, u, v, x_sol, y_sol, speed_sq = solve_ode_for_trajectory(OMEGA_POS, x0, y0, u0, v0)
ax2.plot(x_sol, y_sol, label='E2.2 (x0=1,y0=0.5,...)', linewidth=2, color='saddlebrown')
ax2.plot(x0, y0, 'o', color='saddlebrown', markersize=7, markeredgecolor='black', zorder=5) # Start point
add_trajectory_arrows(ax2, x_sol, y_sol, 'saddlebrown')

# Plot theoretical center for E2.2
if speed_sq > 1e-12 and abs(OMEGA_POS) > 1e-9:
    xc_th = x0 + v0 / (2 * OMEGA_POS)
    yc_th = y0 - u0 / (2 * OMEGA_POS)
    ax2.plot(xc_th, yc_th, 'x', color='saddlebrown', markersize=8, mew=1.5, zorder=5) # Center point

ax2.legend()
fig2.tight_layout()
fig2.savefig('Рисунок_2.png', dpi=300) # Save the figure

# --- Experiment 3: Influence of angular velocity ---
fig3, ax3 = plt.subplots(figsize=(8, 8))
ax3.set_title(f'Рис. 3: Влияние величины ω на траекторию (u0=1, v0=0)')
ax3.set_xlabel('x, м')
ax3.set_ylabel('y, м')
ax3.grid(True)
ax3.axis('equal')

u0_e3, v0_e3, x0_e3, y0_e3 = 1.0, 0.0, 0.0, 0.0

omegas_for_e3 = [
    {"val": OMEGA_POS, "clr": "blue", "lbl": f"E3.1 (ω≈{OMEGA_POS:.3f})"},
    {"val": OMEGA_POS * 2, "clr": "red", "lbl": f"E3.2 (ω≈{OMEGA_POS * 2:.3f})"},
    {"val": OMEGA_POS / 2, "clr": "purple", "lbl": f"E3.3 (ω≈{OMEGA_POS / 2:.3f})"},
]

for exp in omegas_for_e3:
    t, u, v, x_sol, y_sol, speed_sq = solve_ode_for_trajectory(
        exp["val"], x0_e3, y0_e3, u0_e3, v0_e3
    )
    ax3.plot(x_sol, y_sol, label=exp["lbl"], linewidth=2, color=exp["clr"])
    ax3.plot(x0_e3, y0_e3, 'o', color=exp["clr"], markersize=7, markeredgecolor='black', zorder=5) # Start point
    add_trajectory_arrows(ax3, x_sol, y_sol, exp["clr"])

    # Plot theoretical center
    if speed_sq > 1e-12 and abs(exp["val"]) > 1e-9:
        xc_th = x0_e3 + v0_e3 / (2 * exp["val"])
        yc_th = y0_e3 - u0_e3 / (2 * exp["val"])
        ax3.plot(xc_th, yc_th, 'x', color=exp["clr"], markersize=8, mew=1.5, zorder=5) # Center point

ax3.legend()
fig3.tight_layout()
fig3.savefig('Рисунок_3.png', dpi=300) # Save the figure

# --- Plot for Conservation of Energy E(t) ---
fig4, ax4 = plt.subplots(figsize=(10, 4))
if t_for_E is not None and initial_speed_sq_for_E is not None and initial_speed_sq_for_E > 1e-12:
    E_sol = (u_for_E ** 2 + v_for_E ** 2) / initial_speed_sq_for_E
    max_dev = np.max(np.abs(E_sol - 1.0))
    ax4.plot(t_for_E, E_sol, label=f'Числ. решение (max|E-1|≈{max_dev:.1e})', lw=2, c='darkcyan')
    ax4.set_title(f'Рис. 4: Относительное изменение E(t) для E1.1 (u0=1,v0=0,ω≈{OMEGA_POS:.3f})')
    ax4.set_xlabel('Время t, с')
    ax4.set_ylabel('E(t) = (u² + v²) / (u₀² + v₀²)')
    
    # Set y-axis limits to clearly show deviation, but keep it centered around 1.0
    disp_range = max(1e-8, max_dev * 1.5) if max_dev > 1e-15 else 1e-10
    ax4.set_ylim(1.0 - disp_range, 1.0 + disp_range)
    
    ax4.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='both'))
    ax4.yaxis.set_major_formatter(mticker.FormatStrFormatter('%.8f')) # Show more decimal places

    ax4.axhline(1.0, color='gray', linestyle='--', lw=0.8, label='E=1 (теор.)')
    ax4.legend()
    ax4.grid(True)
    fig4.tight_layout()
    fig4.savefig('Рисунок_4.png', dpi=300) # Save the figure

plt.show()