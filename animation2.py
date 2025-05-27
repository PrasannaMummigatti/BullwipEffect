import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib.animation import FuncAnimation

# Parameters
T = 20
mu = 50
sigma = 3
r = 0.4
p = 5
z = 1.65
lead_times = [1, 2, 3, 4, 5]

# Generate consistent demand
np.random.seed(100)
demand = [mu]
for t in range(1, T):
    e_t = np.random.normal(0, sigma)
    demand.append(mu + r * demand[-1] + e_t)
demand = np.array(demand)

x = np.arange(T)
x_smooth = np.linspace(p, T - 1, 300)
demand_spline = make_interp_spline(x, demand)(x_smooth)

# Set up figure
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor("lightyellow") 
ax.set_facecolor("lightyellow")
ax.set_xlim(p, T)
ax.set_ylim(40, 180)
ax.set_title('Retailer Orders vs. Customer Demand\n(Lead Time Accumulation)', fontsize=14)
ax.set_xlabel('Time Period')
ax.set_ylabel('Units Ordered')
ax.grid(False)
fig_manager = plt.get_current_fig_manager()
fig_manager.window.wm_geometry(f"+{100}+{100}")

# Remove border spines
for spine in ax.spines.values():
    spine.set_visible(False)

# Static customer demand
ax.plot(x_smooth, demand_spline, 'k--', linewidth=2, label='Customer Demand')
ax.legend(loc='upper right', frameon=True, facecolor='lightyellow', edgecolor='none')
# Annotation for current lead time
text_lead = ax.text(0.05, 0.9, '', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8))

# Store the plotted lines to avoid duplicates
plotted_leads = set()

def update(frame):
    if frame == -1:
        # Initial delay frame: only show demand
        #text_lead.set_text('Customer Demand Shown...')
        return [text_lead]

    L = lead_times[frame]

    if L in plotted_leads:
        return []

    forecast_mean = np.zeros(T)
    forecast_std = np.zeros(T)
    order_up_to = np.zeros(T)
    orders = np.zeros(T)

    for t in range(p, T):
        window = demand[t - p:t]
        forecast_mean[t] = np.mean(window) * L
        forecast_std[t] = np.std(window) * np.sqrt(L)
        order_up_to[t] = forecast_mean[t] + z * forecast_std[t]
        orders[t] = order_up_to[t] - order_up_to[t - 1] + demand[t - 1]

    orders_spline = make_interp_spline(x, orders)(x_smooth)

    # Plot orders
    line, = ax.plot(x_smooth, orders_spline, label=f'Orders (LeadTime={L})', linewidth=1.5)
    plotted_leads.add(L)

    #text_lead.set_text(f'Lead Time: L = {L}')
    ax.legend(loc='upper right', frameon=True, facecolor='lightyellow', edgecolor='none')

    return [line, text_lead]

# Animate (include frame = -1 for delay)
ani = FuncAnimation(
    fig,
    update,
    frames=[-1] + list(range(len(lead_times))),
    interval=1500,  # 1.5 seconds per frame
    blit=False,
    repeat=False
)

plt.tight_layout()
plt.show()
