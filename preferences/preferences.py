# import sys
import logging
# import json
# from cryptography.fernet import Fernet
# from pykeepass import PyKeePass

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QTableView, QHeaderView, QFileDialog, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
from preferences.UI.preferences_ui import Ui_Dialog

class Preferences_Dialog(QDialog, Ui_Dialog):
    def __init__(self, prefFiles):
        super().__init__()
        self.setupUi(self)

        # Logging stuf
        self.logger = logging.getLogger(self.__class__.__name__)
        # self.logger.setLevel(logging.DEBUG)

        self.resize(700, 460)
        # Variables diverses
        self.prefFiles = prefFiles
        self.lb_Pref = list()
        self.le_Pref = list()
        self.prefs = list()
        self.cancelSelected = False
        self.prefs_modified = False
        self.apps = self.prefFiles.get("apps", {})
        self.keepassFiles = self.prefFiles.get("kbdxFiles", None)
        
        self.previously_selected_app = None
        self.previously_selected_kbdx = None
        
        self.logger.debug(f"self.prefFiles = {list(self.prefFiles.keys())}")
        self.logger.debug(f"self.apps = {list(self.apps.keys())}")
        self.logger.debug(f"self.keepassFiles = {list(self.keepassFiles.keys()) if self.keepassFiles else None}")

        # Affichage de la liste des applications dans tv_apps
        self.appsModel = QStandardItemModel()
        self.appsModel.setHorizontalHeaderLabels(["Nom", "Chemin du binaire", "Arguments", "Port"])
        self.tv_apps.setSelectionBehavior(QTableView.SelectRows)
        self.tv_apps.setSelectionMode(QTableView.SingleSelection)
        self.tv_apps.setEditTriggers(QTableView.NoEditTriggers)
        if self.apps:
            for app_name, app_info in self.apps.items():
                # Créer une ligne
                name_item = QStandardItem(app_name)
                bin_item = QStandardItem(app_info["bin"])
                args_item = QStandardItem(app_info["args"])
                port_item = QStandardItem(app_info.get("port", ""))
                self.appsModel.appendRow([name_item, bin_item, args_item, port_item])
        self.tv_apps.setModel(self.appsModel)
        self.tv_apps.verticalHeader().setVisible(False)
        self.tv_apps.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tv_apps.resizeColumnsToContents()
        self.tv_apps.resizeRowsToContents()
        
        # Affichage de la liste des fichiers Keepass dans tv_kbdx
        self.kbdxModel = QStandardItemModel()
        self.kbdxModel.setHorizontalHeaderLabels(["Nom", "Chemin du fichier"])
        self.tv_kbdx.setSelectionBehavior(QTableView.SelectRows)
        self.tv_kbdx.setSelectionMode(QTableView.SingleSelection)
        self.tv_kbdx.setEditTriggers(QTableView.NoEditTriggers)
        if self.keepassFiles:
            for kbdx_name in self.keepassFiles.keys():
                # Créer une ligne
                name_item = QStandardItem(kbdx_name)
                path_item = QStandardItem(self.keepassFiles[kbdx_name]["file"])
                self.kbdxModel.appendRow([name_item, path_item])
        self.tv_kbdx.setModel(self.kbdxModel)
        self.tv_kbdx.verticalHeader().setVisible(False)
        self.tv_kbdx.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tv_kbdx.resizeColumnsToContents()
        
        
        # Connecteurs des boutons et des tableaux
        self.pb_appsadd.clicked.connect(self.addApp)
        self.pb_appsdel.clicked.connect(self.delApp)
        self.pb_appspath.clicked.connect(self.selectAppPath)
        self.pb_kbdxadd.clicked.connect(self.addKbdx)
        self.pb_kbdxdel.clicked.connect(self.delKbdx)
        self.pb_kbdxpath.clicked.connect(self.selectKbdxPath)
        self.tv_apps.clicked.connect(self.on_apps_selection_clicked)
        self.tv_kbdx.clicked.connect(self.on_kbdx_selection_clicked)
        
    def addApp(self):
        """Affiche la boîte de dialogue d'ajout d'une application
        """
        check_apps = self.appsModel.findItems(self.le_appsname.text(), column=0)
        if check_apps:
            self.logger.warning(f"Modifying app '{self.appsModel.item(check_apps[0].row(), 0).text()}'")
            if self.appsModel.item(check_apps[0].row(), 1).text() != self.le_appspath.text():
                self.logger.warning(f"Modifying '{self.le_appsname.text()}' app's path from '{self.appsModel.item(check_apps[0].row(), 1).text()}' to '{self.le_appspath.text()}'")
                self.appsModel.item(check_apps[0].row(), 1).setText(self.le_appspath.text())
            elif self.appsModel.item(check_apps[0].row(), 2).text() != self.le_appsargs.text():
                self.logger.warning(f"Modifying '{self.le_appsname.text()}' app's args from '{self.appsModel.item(check_apps[0].row(), 2).text()}' to '{self.le_appsargs.text()}'")
                self.appsModel.item(check_apps[0].row(), 2).setText(self.le_appsargs.text())
            else:
                self.logger.warning(f"App '{self.le_appsname.text()}' already exists. No modification needed.")
        else:
            name_item = QStandardItem(self.le_appsname.text())
            bin_item = QStandardItem(self.le_appspath.text())
            args_item = QStandardItem(self.le_appsargs.text())
            port_item = QStandardItem(self.le_appsport.text())
            self.appsModel.appendRow([name_item, bin_item, args_item, port_item])
            self.logger.warning(f"New app '{self.le_appsname.text()}' added.")
        self.le_appsname.clear()
        self.le_appspath.clear()
        self.le_appsargs.clear()
        self.le_appsport.clear()
        self.save_preferences()
    
    def delApp(self):
        """Affiche la boîte de dialogue de suppression d'une application
        """
        self.logger.info("delApp called")
        check_apps = self.appsModel.findItems(self.le_appsname.text(), column=0)
        if check_apps:
            self.logger.warning(f"Deleting app '{self.appsModel.item(check_apps[0].row(), 0).text()}'")
            self.appsModel.removeRow(check_apps[0].row())
        else:
            self.logger.warning(f"App '{self.le_appsname.text()}' not found. No deletion needed.")
        self.le_appsname.clear()
        self.le_appspath.clear()
        self.le_appsargs.clear()
        self.save_preferences()
    
    def selectAppPath(self):
        """Affiche la boîte de dialogue de sélection du chemin d'une application
        """
        file_path, filter = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier",  # Titre de la fenêtre
            "",                         # Répertoire de départ (vide pour répertoire courant)
            "Tous les fichiers (*)"     # Filtre des fichiers
        )
        if file_path:
            self.le_appspath.setText(file_path)
    
    def addKbdx(self):
        """Affiche la boîte de dialogue d'ajout d'un fichier KeePass
        """
        self.logger.info("addKbdx called")
        check_kbdx = self.kbdxModel.findItems(self.le_kbdxname.text(), column=0)
        if check_kbdx:
            self.logger.warning(f"Modifying kbdx '{self.kbdxModel.item(check_kbdx[0].row(), 0).text()}'")
            if self.kbdxModel.item(check_kbdx[0].row(), 1).text() != self.le_kbdxpath.text():
                self.logger.warning(f"Modifying '{self.le_kbdxname.text()}' kbdx's path from '{self.kbdxModel.item(check_kbdx[0].row(), 1).text()}' to '{self.le_kbdxpath.text()}'")
                self.kbdxModel.item(check_kbdx[0].row(), 1).setText(self.le_kbdxpath.text())
            else:
                self.logger.warning(f"Kbdx '{self.le_kbdxname.text()}' already exists. No modification needed.")
        else:
            name_item = QStandardItem(self.le_kbdxname.text())
            bin_item = QStandardItem(self.le_kbdxpath.text())
            self.kbdxModel.appendRow([name_item, bin_item])
            self.logger.warning(f"New kbdx '{self.le_kbdxname.text()}' added.")
        self.le_kbdxname.clear()
        self.le_kbdxpath.clear()
        self.save_preferences()
        
    def delKbdx(self):
        """Affiche la boîte de dialogue de suppression d'un fichier KeePass
        """
        self.logger.info("delKbdx called")
        check_kbdx = self.kbdxModel.findItems(self.le_kbdxname.text(), column=0)
        if check_kbdx:
            self.logger.warning(f"Deleting kbdx '{self.kbdxModel.item(check_kbdx[0].row(), 0).text()}'")
            self.kbdxModel.removeRow(check_kbdx[0].row())
        else:
            self.logger.warning(f"Kbdx '{self.le_kbdxname.text()}' not found. No deletion needed.")
        self.le_kbdxname.clear()
        self.le_kbdxpath.clear()
        self.save_preferences()
    
    def selectKbdxPath(self):
        """Affiche la boîte de dialogue de sélection du chemin d'un fichier KeePass
        """
        self.logger.info("selectKbdxPath called")
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner un fichier",  # Titre de la fenêtre
            "",                          # Répertoire de départ (vide pour répertoire courant)
            "Fichiers KeePass (*.kdbx);;Tous les fichiers (*)"  # Filtre des fichiers
        )
        if file_path:
            self.le_kbdxpath.setText(file_path)

    def on_apps_selection_clicked(self, index):
        """Affiche la boîte de dialogue de suppression d'une application
        """
        if index.isValid():
            name = self.appsModel.item(index.row(), 0).text()
            bin = self.appsModel.item(index.row(), 1).text()
            args = self.appsModel.item(index.row(), 2).text()
            port = self.appsModel.item(index.row(), 3).text() if self.appsModel.columnCount() > 3 else ""
            if self.previously_selected_app is None or self.previously_selected_app != index.row():
                self.previously_selected_app = index.row()
                
                self.le_appsname.setText(name)
                self.le_appspath.setText(bin)
                self.le_appsargs.setText(args)
                self.le_appsport.setText(port)
                self.logger.info(f"Selected app: {name}")
            else:
                self.tv_apps.selectionModel().clearSelection()
                self.le_appsname.clear()
                self.le_appspath.clear()
                self.le_appsargs.clear()
                self.le_appsport.clear()
                self.logger.info(f"Deselected the currently selected app: {name}")
                self.previously_selected_app = None
        else:
            self.logger.info("No app selected")
            self.previously_selected_app = None

    def on_kbdx_selection_clicked(self, index):
        """Affiche la boîte de dialogue de suppression d'un fichier KeePass
        """
        if index.isValid():
            name = self.kbdxModel.item(index.row(), 0).text()
            path = self.kbdxModel.item(index.row(), 1).text()
            if self.previously_selected_kbdx is None or self.previously_selected_kbdx != index.row():
                self.previously_selected_kbdx = index.row()
                
                self.le_kbdxname.setText(name)
                self.le_kbdxpath.setText(path)
                self.logger.info(f"Selected kbdx: {name}")
            else:
                self.tv_kbdx.selectionModel().clearSelection()
                self.le_kbdxname.clear()
                self.le_kbdxpath.clear()
                self.logger.info(f"Deselected the currently selected kbdx: {name}")
                self.previously_selected_kbdx = None
        else:
            self.logger.info("No kbdx selected")
            self.previously_selected_kbdx = None
            
    def save_preferences(self):
        """Sauvegarde les préférences dans le dictionnaire self.prefFiles
        """
        self.logger.info("save_preferences called")
        # Sauvegarde des applications
        apps_dict = {}
        for row in range(self.appsModel.rowCount()):
            name = self.appsModel.item(row, 0).text()
            bin = self.appsModel.item(row, 1).text()
            args = self.appsModel.item(row, 2).text()
            port = self.appsModel.item(row, 3).text() if self.appsModel.columnCount() > 3 else ""
            apps_dict[name] = {"bin": bin, "args": args, "port": port}
        self.prefFiles["apps"] = apps_dict
        self.logger.debug(f"Saved apps: {list(apps_dict.keys())}")
        # Sauvegarde des fichiers KeePass
        kbdx_dict = {}
        for row in range(self.kbdxModel.rowCount()):        
            name = self.kbdxModel.item(row, 0).text()
            path = self.kbdxModel.item(row, 1).text()
            if name not in self.prefFiles["kbdxFiles"].keys():
                self.prefFiles["kbdxFiles"][name] = {"file": path, "password": '', "ciphered": False, "valid": False, "index": row}
            kbdx_dict[name] = {"file": path}
        # self.prefFiles["kbdx"] = kbdx_dict
        # dict1 = {k: v for k, v in dict1.items() if k in dict2}
        self.prefFiles["kbdxFiles"] = {k: v for k, v in self.prefFiles["kbdxFiles"].items() if k in kbdx_dict.keys()}
        self.logger.info(f"Saved kbdx: {list(kbdx_dict.keys())}")
        self.prefs_modified = True