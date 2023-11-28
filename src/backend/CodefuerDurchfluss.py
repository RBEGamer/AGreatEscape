from scipy import integrate
import numpy as np

# Konstanten
flussquerschnitt = 3.0 # Tür ist in 2D 3 Meter breit
geschwindigkeit = lambda t: 2.0 * t
zeit_anfang = 0.0 # Das sind Sekunden
zeit_ende = 300.0 # Das sind Sekunden

# Zeitschritt
dt = (zeit_ende - zeit_anfang) / 100

# Durchflussmenge berechnen
durchflussmenge = []
for t in np.arange(zeit_anfang, zeit_ende, dt):
    durchflussmenge.append(flussquerschnitt * geschwindigkeit(t))

# Ausgabe
print("Die Durchflussmenge beträgt:")
for t, durchflussmenge in enumerate(durchflussmenge):
    print("t = {} s : {} m^3/s".format(t * dt, durchflussmenge))

# Ausgabe als 2D-Array
durchflussmenge = np.array(durchflussmenge)
print("Die Durchflussmenge als 2D-Array:")
print(durchflussmenge)