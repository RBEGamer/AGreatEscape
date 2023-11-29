import csv
import random
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from faker import Faker
import heapq

def generiere_namen(anzahl):
    fake = Faker()
    return [fake.name() for _ in range(anzahl)]

def lese_karte_von_csv(dateipfad):
    karte = []
    with open(dateipfad, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        for reihe in csvreader:
            karte.append([int(zelle) if zelle.isdigit() else 0 for zelle in reihe])
    return karte

def zeichne_karte(karte, titel='2D Karte des Konzertgeländes'):
    cmap = mcolors.ListedColormap(['white', 'black', 'red'])
    bounds = [0, 1, 2, 3]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    plt.imshow(karte, cmap=cmap, norm=norm)
    plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), ticks=[0.5, 1.5, 2.5],
                 label='Gelände', spacing='proportional')
    plt.title(titel)
    plt.xlabel('X-Position')
    plt.ylabel('Y-Position')
    plt.grid(which='major', color='gray', linestyle='-', linewidth=0.5)
    plt.show()

def dijkstra(grid, start, ziel):
    rows, cols = len(grid), len(grid[0])
    dist = {(x, y): float('inf') for x in range(rows) for y in range(cols)}
    prev = {start: None}
    dist[start] = 0
    queue = [(0, start)]
    
    while queue:
        d, current = heapq.heappop(queue)
        if current == ziel:
            path = []
            while current:
                path.append(current)
                current = prev[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < rows and 0 <= ny < cols and dist[nx, ny] > d + 1:
                dist[nx, ny] = d + 1
                prev[(nx, ny)] = current
                heapq.heappush(queue, (d + 1, (nx, ny)))

    return []

def finde_wege_und_zeichne_karten(breite, hoehe, namen, ausgang, ausgabe_ordner, karte):
    if not os.path.exists(ausgabe_ordner):
        os.makedirs(ausgabe_ordner)

    schritte_pro_person = {}
    for name in namen:
        start_x, start_y = random.randint(0, breite - 1), random.randint(0, hoehe - 1)
        weg = dijkstra(karte, (start_x, start_y), ausgang)
        schritte_pro_person[name] = len(weg) - 1

        filename = os.path.join(ausgabe_ordner, f'{name.replace(" ", "_")}_daten.csv')
        with open(filename, 'w', newline='', encoding='ISO-8859-1') as csvfile:
            csvfile.write('Schritt;X-Position;Y-Position\n')
            for schritt, (x, y) in enumerate(weg):
                csvfile.write(f'{schritt + 1};{x};{y}\n')

        # Zeichnen der 2D-Karte für jede Person
        plt.figure()
        plt.grid(True)
        plt.plot([x for x, y in weg], [y for x, y in weg], marker='o', linestyle='-', color='red', label='Weg')
        plt.plot(start_x, start_y, marker='o', color='green', label='Start')
        plt.plot(ausgang[0], ausgang[1], marker='x', color='blue', label='Ziel')
        plt.xlim(0, breite - 1)
        plt.ylim(0, hoehe - 1)
        plt.title(f'Weg von {name}')
        plt.legend()
        plt.savefig(os.path.join(ausgabe_ordner, f'{name.replace(" ", "_")}_Karte.png'))
        plt.close()

    return schritte_pro_person

def main():
    modus = input("Möchten Sie eine Karte einlesen (E) oder eine neue Karte generieren (G)? [E/G]: ").strip().upper()
    ausgabe_ordner = 'D:/Hackathon/UltimativerTest3'  # Hier den Ordnerpfad anpassen

    if modus == "E":
        dateipfad = input("Bitte geben Sie den Pfad zur Karten-CSV-Datei ein: ")
        karte = lese_karte_von_csv(dateipfad)
        breite, hoehe = len(karte[0]), len(karte)
        zeichne_karte(karte)
    else:
        breite = int(input("Bitte geben Sie die Breite des Konzertbereichs ein: "))
        hoehe = int(input("Bitte geben Sie die Höhe des Konzertbereichs ein: "))
        karte = [[0 for _ in range(breite)] for _ in range(hoehe)]

    anzahl_personen = int(input("Bitte geben Sie die Anzahl der Personen ein: "))
    namen = generiere_namen(anzahl_personen)
    ausgang = (random.randint(0, breite - 1), random.randint(0, hoehe - 1))
    schritte = finde_wege_und_zeichne_karten(breite, hoehe, namen, ausgang, ausgabe_ordner, karte)

    for name, anzahl_schritte in schritte.items():
        print(f"{name} ist insgesamt {anzahl_schritte} Schritte gegangen.")

if __name__ == "__main__":
    main()