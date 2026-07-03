import sys
import os
import json

# Sprawdzenie liczby argumentów
if len(sys.argv) != 3:
    print("Użycie programu:")
    print("python project.py plik_wejściowy plik_wyjściowy")
    exit()

# Pobranie nazw plików
input_file = sys.argv[1]
output_file = sys.argv[2]

# Sprawdzenie czy plik wejściowy istnieje
if not os.path.exists(input_file):
    print("Błąd! Plik wejściowy nie istnieje.")
    exit()

print("Plik wejściowy:", input_file)
print("Plik wyjściowy:", output_file)

try:
    with open(input_file, "r", encoding="utf-8") as file:
        dane = json.load(file)

    print("Plik JSON został poprawnie wczytany.")
    print(dane)

except json.JSONDecodeError:
    print("Błąd! Niepoprawna składnia pliku JSON.")