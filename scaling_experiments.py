import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np

# Broj procesa za testiranje
process_counts = [1, 2, 4, 8]

# Broj simulacija (za "jako skaliranje" je fiksno)
num_simulations = 8

# Broj ponavljanja za svaku konfiguraciju (da se dobije prosečno vreme)
repetitions = 30


def run_simulation(num_processes):
    """Pokreće paralelnu simulaciju sa datim brojem procesa i meri vreme izvršavanja."""
    start = time.time()
    subprocess.run(["python", "double_pendulum_par.py", str(num_processes)],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    end = time.time()
    return end - start


# ----------------------- JAKO SKALIRANJE -----------------------
strong_scaling_times = {}

print("Pokrećem test jakog skaliranja...")
for p in process_counts:
    total_time = 0
    for _ in range(repetitions):
        # privremeno menjaš broj procesa unutar koda pre pokretanja
        with open("double_pendulum_par.py", "r", encoding="utf-8") as f:
            code = f.read()
        new_code = code.replace("processes=4", f"processes={p}")
        with open("double_pendulum_par.py", "w", encoding="utf-8") as f:
            f.write(new_code)

        total_time += run_simulation(p)

        # vraćanje originalne vrednosti (4 procesa)
        with open("double_pendulum_par.py", "w", encoding="utf-8") as f:
            f.write(code)

    avg_time = total_time / repetitions
    strong_scaling_times[p] = avg_time
    print(f"Procesa: {p} → prosečno vreme: {avg_time:.2f}s")

# Ubrzanje
T1 = strong_scaling_times[1]
speedups = {p: T1 / t for p, t in strong_scaling_times.items()}


# ----------------------- CRTANJE GRAFA (Amdal) -----------------------
plt.figure(figsize=(8, 5))
x = list(speedups.keys())
y = list(speedups.values())
ideal = x  # idealna linija (y=x)

plt.plot(x, y, 'o-', label="Dobijeno ubrzanje")
plt.plot(x, ideal, '--', label="Idealno skaliranje (y = x)")
plt.xlabel("Broj procesa")
plt.ylabel("Ubrzanje (T1/Tp)")
plt.title("Jako skaliranje (Amdalov zakon)")
plt.legend()
plt.grid(True)
plt.savefig("strong_scaling.png")
plt.close()
print("Grafik jakog skaliranja sačuvan kao strong_scaling.png")

# ----------------------- SLABO SKALIRANJE -----------------------

print("\n Pokrećem test slabog skaliranja...")

weak_scaling_times = {}

for p in process_counts:
    total_time = 0
    for _ in range(repetitions):
        # promeni broj simulacija u skladu sa brojem procesa
        num_sims = num_simulations * p

        # menja kod dinamički
        with open("double_pendulum_par.py", "r", encoding="utf-8") as f:
            code = f.read()
        new_code = code.replace("initial_conditions = [",
                                f"initial_conditions = [  # {num_sims} simulacija\n")
        with open("double_pendulum_par.py", "w", encoding="utf-8") as f:
            f.write(new_code)

        total_time += run_simulation(p)

        # vraćanje originala
        with open("double_pendulum_par.py", "w", encoding="utf-8") as f:
            f.write(code)

    avg_time = total_time / repetitions
    weak_scaling_times[p] = avg_time
    print(f"Procesa: {p} → prosečno vreme: {avg_time:.2f}s")

# Efikasnost (idealno bi trebalo da bude 1)
T1_weak = weak_scaling_times[1]
efficiency = {p: T1_weak / t for p, t in weak_scaling_times.items()}

# ----------------------- CRTANJE GRAFA (Gustafson) -----------------------
plt.figure(figsize=(8, 5))
x = list(efficiency.keys())
y = list(efficiency.values())
ideal = [1 for _ in x]

plt.plot(x, y, 'o-', label="Dobijena efikasnost")
plt.plot(x, ideal, '--', label="Idealno skaliranje (y = 1)")
plt.xlabel("Broj procesa")
plt.ylabel("Efikasnost (T1/Tp)")
plt.title("Slabo skaliranje (Gustafsonov zakon)")
plt.legend()
plt.grid(True)
plt.savefig("weak_scaling.png")
plt.close()
print("Grafik slabog skaliranja sačuvan kao weak_scaling.png")
