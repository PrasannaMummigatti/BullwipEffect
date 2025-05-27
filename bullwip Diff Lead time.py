import numpy as np
import matplotlib.pyplot as plt

# Simulation settings
T = 200                 # Time periods
mu = 50                 # Base demand level
sigma = 5               # Std. deviation of noise
r = 0                   # Correlation in demand (as in Figure 2, r = 0)
z = 0                   # No safety stock, to match theoretical lower bound

# Parameters to test
L_values = [1, 2, 3,4,5]    # Lead times
p_values = list(range(1, 10))  # Moving average window sizes

# AR(1) demand generation function
def generate_demand(T, mu, sigma, r):
    demand = [mu]
    for _ in range(1, T):
        e_t = np.random.normal(0, sigma)
        demand.append(mu + r * demand[-1] + e_t)
    return np.array(demand)

# Simulate Bullwhip effect for combinations of L and p
bullwhip_data = {L: [] for L in L_values}

for L in L_values:
    for p in p_values:
        demand = generate_demand(T, mu, sigma, r)
        forecast_mean = np.zeros(T)
        order_up_to = np.zeros(T)
        orders = np.zeros(T)

        for t in range(p, T):
            window = demand[t-p:t]
            forecast_mean[t] = np.mean(window) * L  # forecast lead-time demand
            order_up_to[t] = forecast_mean[t]  # no safety stock

            orders[t] = order_up_to[t] - order_up_to[t-1] + demand[t-1]  # as per paper

        # Trim initial zeros
        demand_var = np.var(demand[p:])
        order_var = np.var(orders[p:])
        bullwhip_ratio = order_var / demand_var
        bullwhip_data[L].append(bullwhip_ratio)

# Plotting
plt.figure(figsize=(10, 6),facecolor='lightyellow')
for L in L_values:
    plt.plot(p_values, bullwhip_data[L], marker='o', label=f'Lead Time L={L}')

plt.title('Bullwhip Effect Magnitude vs. Moving Average Window Size (p)')
plt.xlabel('Moving Average Window Size (p)')
plt.ylabel('Var(Orders) / Var(Demand)')
plt.legend(loc='upper right', frameon=True, facecolor='lightyellow', edgecolor='none')

plt.gca().set_facecolor('lightyellow')
plt.grid(True)
plt.grid(False)
plt.tight_layout()
plt.show()
