import sys
import os
import json
import yaml

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
    # Wczytanie danych
    if input_file.endswith(".json"):
        with open(input_file, "r", encoding="utf-8") as file:
            dane = json.load(file)

    elif input_file.endswith(".yaml") or input_file.endswith(".yml"):
        with open(input_file, "r", encoding="utf-8") as file:
            dane = yaml.safe_load(file)

    else:
        print("Nieobsługiwany format pliku wejściowego.")
        exit()

    print("Plik został poprawnie wczytany.")

    # Zapis danych
    if output_file.endswith(".json"):
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(dane, file, indent=4, ensure_ascii=False)

    elif output_file.endswith(".yaml") or output_file.endswith(".yml"):
        with open(output_file, "w", encoding="utf-8") as file:
            yaml.dump(dane, file, allow_unicode=True, sort_keys=False)

    else:
        print("Nieobsługiwany format pliku wyjściowego.")
        exit()

    print("Plik został zapisany.")

except FileNotFoundError:
    print("Błąd! Nie znaleziono pliku.")

except json.JSONDecodeError:
    print("Błąd! Niepoprawna składnia pliku JSON.")

except yaml.YAMLError:
    print("Błąd! Niepoprawna składnia pliku YAML.")