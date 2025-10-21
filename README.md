# Projekat: Double Pendulum Simulation

## Ocena
Radim projekat za **ocenu 7**.

## Opis problema
Cilj ovog projekta je simulacija dinamike **dvostrukog klatna** (double pendulum), sistema koji se sastoji od dva povezana klatna, pri čemu je kretanje jednog klatna nelinearno povezano sa kretanjem drugog. Problem je poznat po svojoj **osetljivosti na početne uslove** i **kaotičnom ponašanju**.

Simulacija uključuje izračunavanje kretanja po iteracijama, uz primenu osnovnih principa klasične mehanike (Lagrangeova jednačina).

## Metode korišćene za rešavanje problema
Za rešavanje problema korišćene su sledeće metode i pristupi u Python-u:

1. **Sekvencijalna implementacija**
   - Izračunava stanje dvostrukog klatna po iteracijama.
   - Generiše izlazne datoteke (`.csv`) sa rezultatima.

2. **Paralelizovana implementacija**
   - Korišćenjem `multiprocessing` biblioteke.
   - Omogućava ubrzanje izvođenja simulacije pri većem broju iteracija.
   - Rezultati su takođe generisani u `.csv` datotekama.

3. **Eksperimenti skaliranja**
   - **Jako skaliranje (strong scaling)**: upoređivanje ubrzanja paralelne verzije u odnosu na sekvencijalnu.
   - **Slabo skaliranje (weak scaling)**: upoređivanje ubrzanja paralelne verzije uz konstantan posao po procesorskom jezgru.
   - Svaka kombinacija broja jezgara i veličine problema izvršena je 3 puta kako bi se dobili relevantni rezultati.
   - Rezultati su predstavljeni grafički i tabelarno, uključujući prosečno vreme izvršavanja, standardnu devijaciju i outlier-e.


## Pokretanje simulacije
 

### Sekvencijalna verzija
python double_pendulum_seq.py

### Paralelna verzija
python double_pendulum_par.py



Rezultati će biti generisani u `.csv` datotekama koje sadrže stanje sistema po iteracijama.

## Eksperimenti i analize
- Grafici su generisani direktno u root direktorijumu repozitorijuma:
  - `strong_scaling.png` → grafik jakog skaliranja (Amdalov zakon)
  - `weak_scaling.png` → grafik slabog skaliranja (Gustafsonov zakon)
- Za svaki grafikon:
  - X-osa prikazuje broj procesa.
  - Y-osa prikazuje ostvareno ubrzanje ili efikasnost.
- Analiza uključuje poređenje sa idealnim skaliranjem i objašnjenje razlika.

## Biblioteke i alati
- Python: `numpy`, `matplotlib`, `multiprocessing`
- Eksperimenti su rađeni na mašini sa:
  - CPU: AMD Ryzen 7 7800X3D, 8 jezgara
  - RAM: 32 GB
  - OS: Windows 11
