# Projekat: Double Pendulum Simulation

## Ocena
Radim projekat za **ocenu 7**.

## Opis problema
**Dvostruko klatno** je sistem od dva povezana klatna koji se slobodno kreću pod uticajem gravitacije.  
Ovo je klasičan primer **nelinearnog i kaotičnog sistema**, gde mala promena početnih uslova dovodi do značajno različitih trajektorija.

### Varijable
- θ1, θ2 – uglovi klatna u odnosu na vertikalu (radijani)

- ω1, ω2 – ugaone brzine klatna (rad/s)

- L1, L2 – dužine klatna (m)

- M1, M2 – mase klatna (kg)

- g – gravitaciona konstanta (m/s²)

### Diferencijalne jednačine
Koriste se Lagrangeove jednačine:

dθ1/dt = ω1
dθ2/dt = ω2
dω1/dt = (M2*L1*ω1^2*sin(θ2-θ1)*cos(θ2-θ1) + M2*g*sin(θ2)*cos(θ2-θ1)
          + M2*L2*ω2^2*sin(θ2-θ1) - (M1+M2)*g*sin(θ1)) 
          / ((M1+M2)*L1 - M2*L1*cos^2(θ2-θ1))
dω2/dt = -(L2/L1)*ω1^2*sin(θ2-θ1) + ((M1+M2)*g*sin(θ1)*cos(θ2-θ1))/L2
          - ((M1+M2)*g*sin(θ2))/L2 + (M1+M2)*ω2^2*sin(θ2-θ1)*cos(θ2-θ1)

## Implementacija u Python-u

1. **Sekvencijalna verzija**
   - Rešava sistem ODE koristeći `odeint` iz `scipy.integrate`.
   - Početni uslovi: θ1 = θ2 = π/2, ω1 = ω2 = 0
   - Generiše **jedan CSV fajl** `results_sequential.csv` sa kolonama: `time, theta1, theta2, x1, y1, x2, y2`
   - Pozicije klatna:  
        - x1 = L1 * sin(θ1)
        - y1 = -L1 * cos(θ1)
        - x2 = x1 + L2 * sin(θ2)
        - y2 = y1 - L2 * cos(θ2)

2. **Paralelizovana verzija**
   - Korišćenjem `multiprocessing.Pool`.
   - Izvršava više simulacija sa različitim početnim uglovima paralelno.
   - Rezultati se čuvaju u više CSV fajlova (`results_parallel_1.csv`, `results_parallel_2.csv`, …)
   - Omogućava ubrzanje izvođenja simulacije pri većem broju procesa.

## Eksperimenti skaliranja

1. **Jako skaliranje (strong scaling)**  
   - Upoređuje se vreme paralelne verzije sa sekvencijalnom.
   - Računa se ubrzanje: S_p = T1 / Tp
   - Grafikon sačuvan kao `strong_scaling.png`.
   - Svaka kombinacija broja jezgara izvršena 30 puta.

2. **Slabo skaliranje (weak scaling)**  
   - Posao po jezgru je konstantan.
   - Računa se ubrzanje: S_p = T1 / Tp
   - Grafikon sačuvan kao `weak_scaling.png`.

## Pokretanje simulacija

### Sekvencijalna verzija
python sequential_simulation.py

### Paralelna verzija
python parallel_simulation.py

CSV fajlovi će sadržati stanje sistema po iteracijama.

## Biblioteke i alati
- Python: `numpy`, `matplotlib`, `multiprocessing`
- Eksperimenti su rađeni na mašini sa:
  - CPU: AMD Ryzen 7 7800X3D, 8 jezgara
  - RAM: 32 GB
  - OS: Windows 11
