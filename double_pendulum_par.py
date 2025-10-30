import numpy as np
from scipy.integrate import odeint
from multiprocessing import Pool
import csv
import time

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
    ω1_dot = (M2 * L1 * ω1**2 * np.sin(delta) * np.cos(delta) +
              M2 * g * np.sin(θ2) * np.cos(delta) +
              M2 * L2 * ω2**2 * np.sin(delta) -
              (M1 + M2) * g * np.sin(θ1)) / den1
    ω2_dot = (-L2/L1) * ω1**2 * np.sin(delta) + \
             (M1 + M2) * g * np.sin(θ1) * np.cos(delta) / L2 - \
             (M1 + M2) * g * np.sin(θ2) / L2 + \
             (M1 + M2) * ω2**2 * np.sin(delta) * np.cos(delta)

    return [ω1, ω1_dot, ω2, ω2_dot]


# Funkcija za jednu simulaciju
def simulate_double_pendulum(args):
    θ1_0, θ2_0, index = args
    ω1_0, ω2_0 = 0.0, 0.0
    y0 = [θ1_0, ω1_0, θ2_0, ω2_0]
    t = np.linspace(0, 20, 2000)
    sol = odeint(derivatives, y0, t, args=(L1, L2, M1, M2))

    θ1 = sol[:, 0]
    θ2 = sol[:, 2]
    x1 = L1 * np.sin(θ1)
    y1 = -L1 * np.cos(θ1)
    x2 = x1 + L2 * np.sin(θ2)
    y2 = y1 - L2 * np.cos(θ2)

    filename = f"results_parallel_{index}.csv"
    with open(filename, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "theta1", "theta2", "x1", "y1", "x2", "y2"])
        for i in range(len(t)):
            writer.writerow([t[i], θ1[i], θ2[i], x1[i], y1[i], x2[i], y2[i]])

    return filename


if __name__ == "__main__":
    # Pocetni uslovi(uglovi)
    initial_conditions = [
        (np.pi/2, np.pi/2, 1),
        (np.pi/3, np.pi/3, 2),
        (np.pi/4, np.pi/6, 3),
        (np.pi/2, np.pi/4, 4),
        (np.pi/2, np.pi/3, 5),
        (np.pi/3, np.pi/2, 6),
        (np.pi/5, np.pi/3, 7),
        (np.pi/2.5, np.pi/2, 8),
    ]

    start = time.time()
    with Pool(processes=4) as pool:  
        results = pool.map(simulate_double_pendulum, initial_conditions)
    end = time.time()

    print(f"Generisano {len(results)} fajlova.")
    print(f"Ukupno vreme izvrsavanja: {end - start:.2f} sekundi.")