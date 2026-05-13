import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import PySide6

UI_FILE = "main.ui"  # <-- mets ici le chemin vers ton fichier .ui

def load_ui(path):
    loader = QUiLoader()
    ui_file = QFile(path)
    ui_file.open(QFile.ReadOnly)
    widget = loader.load(ui_file)
    ui_file.close()
    return widget

# Diagnostic rapide
print(f"Python  : {sys.version.split()[0]}")
print(f"PySide6 : {PySide6.__version__}")
print(f"Qt      : {PySide6.QtCore.__version__}")

# On désactive l'auto-scaling pour limiter les surprises
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "0"

app = QApplication(sys.argv)

# Container principal
main_window = QWidget()
layout = QHBoxLayout(main_window)

# Chargement en "Fusion"
fusion_app = QApplication.instance()
fusion_app.setStyle("Fusion")
fusion_widget = load_ui(UI_FILE)
layout.addWidget(fusion_widget)

# Revenir au style par défaut
fusion_app.setStyle(QApplication.style().objectName())
default_widget = load_ui(UI_FILE)
layout.addWidget(default_widget)

# Labels pour repérage
layout.addWidget(QLabel("← Style Fusion | Style par défaut →"))

main_window.setWindowTitle("Comparateur visuel d'UI")
main_window.show()

sys.exit(app.exec())
