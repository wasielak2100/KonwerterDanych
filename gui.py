import sys
import json
import yaml
import xml.etree.ElementTree as ET
import threading

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox
)


class Window(QWidget):

    def __init__(self):
        super().__init__()

        self.input_file = ""
        self.output_file = ""

        self.setWindowTitle("Konwerter danych")
        self.resize(400, 200)

        layout = QVBoxLayout()

        self.btnInput = QPushButton("Wybierz plik wejściowy")
        self.btnOutput = QPushButton("Wybierz plik wyjściowy")
        self.btnConvert = QPushButton("Konwertuj")

        layout.addWidget(self.btnInput)
        layout.addWidget(self.btnOutput)
        layout.addWidget(self.btnConvert)

        self.setLayout(layout)

        self.btnInput.clicked.connect(self.chooseInput)
        self.btnOutput.clicked.connect(self.chooseOutput)
        self.btnConvert.clicked.connect(self.startConvert)

    def chooseInput(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz plik",
            "",
            "Data (*.json *.yaml *.yml *.xml)"
        )

        if file:
            self.input_file = file

    def chooseOutput(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz jako",
            "",
            "JSON (*.json);;YAML (*.yaml);;XML (*.xml)"
        )

        if file:
            self.output_file = file

    def startConvert(self):
        thread = threading.Thread(target=self.convert)
        thread.start()

    def convert(self):

        if self.input_file == "" or self.output_file == "":
            QMessageBox.warning(self, "Błąd", "Najpierw wybierz oba pliki.")
            return

        try:

            # Wczytanie danych
            if self.input_file.endswith(".json"):
                with open(self.input_file, "r", encoding="utf-8") as f:
                    dane = json.load(f)

            elif self.input_file.endswith(".yaml") or self.input_file.endswith(".yml"):
                with open(self.input_file, "r", encoding="utf-8") as f:
                    dane = yaml.safe_load(f)

            elif self.input_file.endswith(".xml"):
                tree = ET.parse(self.input_file)
                root = tree.getroot()

                dane = {}

                for element in root:
                    dane[element.tag] = element.text

            else:
                QMessageBox.warning(self, "Błąd", "Nieobsługiwany format.")
                return

            # Zapis danych
            if self.output_file.endswith(".json"):
                with open(self.output_file, "w", encoding="utf-8") as f:
                    json.dump(dane, f, indent=4, ensure_ascii=False)

            elif self.output_file.endswith(".yaml") or self.output_file.endswith(".yml"):
                with open(self.output_file, "w", encoding="utf-8") as f:
                    yaml.dump(dane, f, allow_unicode=True, sort_keys=False)

            elif self.output_file.endswith(".xml"):

                root = ET.Element("data")

                for key, value in dane.items():
                    element = ET.SubElement(root, key)
                    element.text = str(value)

                tree = ET.ElementTree(root)
                tree.write(
                    self.output_file,
                    encoding="utf-8",
                    xml_declaration=True
                )

            else:
                QMessageBox.warning(self, "Błąd", "Nieobsługiwany format wyjściowy.")
                return

            QMessageBox.information(self, "Gotowe", "Konwersja zakończona.")

        except Exception as e:
            QMessageBox.critical(self, "Błąd", str(e))


app = QApplication(sys.argv)

window = Window()
window.show()

sys.exit(app.exec_())