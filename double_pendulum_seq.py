import numpy as np
from scipy.integrate import odeint
import csv

# Fizicke konstante
g = 9.81     
L1 = 1.0     
L2 = 1.0     
M1 = 1.0    
M2 = 1.0    

# Sistem diferencijalnih jednacina
def derivatives(y, t, L1, L2, M1, M2):
    θ1, ω1, θ2, ω2 = y

    delta = θ2 - θ1

    den1 = (M1 + M2) * L1 - M2 * L1 * np.cos(delta)**2
    den2 = (L2/L1) * den1

    ω1_dot = (M2 * L1 * ω1**2 * np.sin(delta) * np.cos(delta) +
              M2 * g * np.sin(θ2) * np.cos(delta) +
              M2 * L2 * ω2**2 * np.sin(delta) -
              (M1 + M2) * g * np.sin(θ1)) / den1

    ω2_dot = (-L2/L1) * ω1**2 * np.sin(delta) + \
              (M1 + M2) * g * np.sin(θ1) * np.cos(delta) / L2 - \
              (M1 + M2) * g * np.sin(θ2) / L2 + \
              (M1 + M2) * ω2**2 * np.sin(delta) * np.cos(delta)

    return [ω1, ω1_dot, ω2, ω2_dot]

# Pocetni uslovi
θ1_0 = np.pi / 2      # pocetni ugao 1 
θ2_0 = np.pi / 2      # pocetni ugao 2 
ω1_0 = 0.0            # pocetna ugaona brzina 1
ω2_0 = 0.0            # pocetna ugaona brzina 2

y0 = [θ1_0, ω1_0, θ2_0, ω2_0]

# Vremenski opseg
t = np.linspace(0, 20, 2000)  # 20 sekundi, 2000 tacaka

# Resavanje sistema
sol = odeint(derivatives, y0, t, args=(L1, L2, M1, M2))

# Izracunavanje pozicija
θ1 = sol[:, 0]
θ2 = sol[:, 2]

x1 = L1 * np.sin(θ1)
y1 = -L1 * np.cos(θ1)

x2 = x1 + L2 * np.sin(θ2)
y2 = y1 - L2 * np.cos(θ2)

# Snimanje u CSV
with open("results_sequential.csv", mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "theta1", "theta2", "x1", "y1", "x2", "y2"])
    for i in range(len(t)):
        writer.writerow([t[i], θ1[i], θ2[i], x1[i], y1[i], x2[i], y2[i]])

print("Rezultati sekvencijalne simulacije su sačuvani u results_sequential.csv")