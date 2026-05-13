from PySide6.QtWidgets import QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget, QLineEdit, QLabel, QFormLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QItemSelectionModel, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sélection/Déselection de ligne")
        self.setup_ui()

    def setup_ui(self):
        # Créer un QTableView
        self.tv_apps = QTableView()

        # Créer un modèle de données
        self.apps_model = QStandardItemModel()
        self.apps_model.setHorizontalHeaderLabels(["Nom", "Chemin du binaire", "Arguments"])

        # Remplir le modèle avec des données d'exemple
        self.apps_model.appendRow([QStandardItem("SSH"), QStandardItem("/usr/bin/ssh"), QStandardItem("")])
        self.apps_model.appendRow([QStandardItem("FileZilla"), QStandardItem("/usr/bin/filezilla"), QStandardItem("--example")])

        # Associer le modèle au QTableView
        self.tv_apps.setModel(self.apps_model)

        # Masquer la colonne de numérotation des lignes
        self.tv_apps.verticalHeader().setVisible(False)

        # Étirer les colonnes pour occuper tout l'espace disponible
        self.tv_apps.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Désactiver l'édition du tableau
        self.tv_apps.setEditTriggers(QTableView.NoEditTriggers)

        # Sélection par ligne complète
        self.tv_apps.setSelectionBehavior(QTableView.SelectRows)

        # Connecter le signal de clic sur une cellule
        self.tv_apps.clicked.connect(self.on_row_clicked)

        # Créer des champs pour afficher les données de la ligne sélectionnée
        self.le_appsname = QLineEdit()
        self.le_appsname.setReadOnly(True)

        self.le_appspath = QLineEdit()
        self.le_appspath.setReadOnly(True)

        self.le_appsargs = QLineEdit()
        self.le_appsargs.setReadOnly(True)

        # Créer un layout pour afficher les données sélectionnées
        form_layout = QFormLayout()
        form_layout.addRow(QLabel("Nom:"), self.le_appsname)
        form_layout.addRow(QLabel("Chemin du binaire:"), self.le_appspath)
        form_layout.addRow(QLabel("Arguments:"), self.le_appsargs)

        # Créer un layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.tv_apps)
        layout.addLayout(form_layout)

        # Créer un widget central et y appliquer le layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def on_row_clicked(self, index):
        # Récupérer la ligne cliquée
        row = index.row()

        # Récupérer les lignes actuellement sélectionnées
        selected_rows = self.tv_apps.selectionModel().selectedRows()

        # Vérifier si la ligne est déjà sélectionnée
        is_row_selected = any(idx.row() == row for idx in selected_rows)

        if is_row_selected:
            # Désélectionner la ligne
            self.tv_apps.clearSelection()
            self.le_appsname.clear()
            self.le_appspath.clear()
            self.le_appsargs.clear()
            print(f"Ligne {row} désélectionnée.")
        else:
            # Sélectionner la ligne
            self.tv_apps.selectionModel().select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

            # Récupérer les données de la ligne
            name = self.apps_model.item(row, 0).text()
            bin_path = self.apps_model.item(row, 1).text()
            args = self.apps_model.item(row, 2).text()

            # Mettre à jour les champs d'affichage
            self.le_appsname.setText(name)
            self.le_appspath.setText(bin_path)
            self.le_appsargs.setText(args)
            print(f"Ligne {row} sélectionnée.")

if __name__ == "__main__":
    from PySide6.QtWidgets import QHeaderView
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
