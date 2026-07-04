#!/usr/bin/python3
import sys
import logging
import json
from pathlib import Path
import subprocess
import re
from copy import deepcopy

from PySide6.QtCore import Qt, QTimer, QObject, QRect
# from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTreeWidgetItem, QMenu, QTreeWidget
from main.UI.main_ui import Ui_MainWindow
from kbdx.kbdx import KBDX_Dialog
from preferences.preferences import Preferences_Dialog

#DONE : dans on_twCnx_itemDoubleClicked
#DONE :     Parser les arguments de la ligne de commande
#DONE :     Lancer la commande avec subprocess.Popen et gérer les erreurs
#DONE :     Effacer les informations sensibles de la mémoire après le lancement de la commande
#DONE :     Isoler run_command dans une fonction à part pour pouvoir l'appeler depuis le menu contextuel avec juste la commande à lancer
#DONE :     Ecrire une fonction pour générer les commandes à passer dans run_command (double clic ou menu contextuel)

#DONE : Gérer le bouton "Ajouter une section" (ajout d'une branche dans l'arborescence)
#DONE :     Qd item sélectionner, ajouter une sous-branche
#DONE :     Qd rien sélectionner, ajouter une branche au niveau racine

#DONE : Gérer le bouton "Ajouter une connexion" (ajout d'une connexion dans l'arborescence)
#DONE :     Qd item sélectionner, ajouter une connexion dans la branche
#DONE :     Qd rien sélectionner, ajouter une connexion au niveau racine

#DONE : Gérér click droit pour lancer le menu contextuel
#DONE :     Affichage des détails de l'item sélectionné
#DONE :     Lancer les actions idoines

#DONE : Gérer le bouton "Supprimer l'objet" (suppression d'une connexion ou de la branche sélectionnée)

#TODO : [Gérer la touche "ENTREE" pour valider les modifications dans les champs]

#TODO : Gérer le fichier de configuration utilisateur (dans le home, ~/.yarcom.qt.conf.json)

#DONE : dans on_twCnx_itemClicked
#DONE :     déplacer un item dans l'arborescence par glisser-déposer
#DONE :     sur une branche permet d'afficher la branche dans les détails pour édition
#DONE :     désélectionne si déjà sélectionné

#DONE : Gérer drag&drop dans l'arborescence
#DONE :     debug dropEvent sous le dernier item d'une branche
#DONE :     gérer évènnement dropEvent
#DONE :     gérer modification dictionnaire
#DONE :     sauvegarder les cnx dans cnx pour éviter de perdre les cnx déplacées
#DONE :         self.yarcom.update_connexions_after_drop()
#DONE :     gérer drops non autorisés :     autorisés :
#DONE :         - branche dans feuille          - branche dans branche
#DONE :         - feuille dans feuille          - feuille dans branche
#TODO :     cf. 2 dernières réponse du chat : https://chat.mistral.ai/chat/cd9846db-fbfe-41a0-9f32-0197247e7029
#DONE :     gérer autres évènements :
#DONE :         - dragEnterEvent
#DONE :         - dragMoveEvent
#DONE :         - dragLeaveEvent

#TODO : Vérifier fonctionnement sur autre OS que Linux (Windows, macOS si possible)
#DONE : Vérifier la sauvegarde lors du déplacement d'items dans l'arborescence (drag&drop) et lors de l'ajout/suppression d'items dans l'arborescence --> update_connexions_after_drop

#TODO : Ajouter icone aux fenêtres password et preferences

logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s - %(filename)s.#%(lineno)d - %(funcName)s - %(levelname)s - %(message)s")

class CustomQTreeWidgetItem(QTreeWidgetItem):
    """Surcharge de QTreeWidgetItem pour ajouter des attributs itemType et itemCnx

    Args:
        QTreeWidgetItem : Classe de base pour les items de l'arborescence
    """
    def __init__(self, name, itemType=None, itemCnx=None):
        super().__init__(name)
        self.itemType = itemType # "branche" ou "cnx" 
        self.itemCnx = itemCnx # None ou dict

class CustomQTreeWidget(QTreeWidget):
    """Surcharge de QTreeWidget pour ajouter des méthodes de gestion des évènements

    Args:
        QTreeWidget : Classe de base pour l'arborescence
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.yarcom = parent

        # Logging stuf
        self.logger = logging.getLogger(self.__class__.__name__)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QTreeWidget.InternalMove)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        
        self.sourceItem = None
        self.targetItem = None

    def mouseMoveEvent(self, event):
        """Gère l'événement de mouvement de la souris pour le drag&drop
        Args:
            event (QMouseEvent): Événement de mouvement de la souris
        """
        # self.logger.info(f"event={event}")
        if event.buttons() == Qt.LeftButton and self.sourceItem is None:
            self.sourceItem = self.itemAt(event.position().toPoint())
            if self.sourceItem is not None:
                self.logger.debug(f"Début du drag&drop pour l'item '{self.sourceItem.text(0)}'")
            else:
                self.logger.debug(f"Début du drag&drop, mais aucun item sous le curseur.")
        super().mouseMoveEvent(event)
    
    def dragEnterEvent(self, event):
        """Surcharge de la méthode de début de déplacement d'un item
        Args:
            event (QMouseEvent): Événement de mouvement de la souris
        """
        # self.logger.info(f"event={event}")
        # self.sourceItem = self.itemAt(event.position().toPoint())
        self.logger.debug(f'sourceItem = {self.sourceItem.text(0) if self.sourceItem else None}, itemType = {self.sourceItem.itemType if self.sourceItem else None}')
        super().dragEnterEvent(event)

    def dragLeaveEvent(self, event):
        """Surcharge de la méthode de fin de déplacement d'un item
        Args:
            event (QMouseEvent): Événement de mouvement de la souris
        """
        # self.logger.info(f"event={event}")
        self.logger.debug(f"Drag&drop annulé, purge de self.sourceItem et self.targetItem en cours ...")
        self.sourceItem = None
        self.targetItem = None
        self.logger.debug(f"Purge de self.sourceItem et self.targetItem terminée.")
        self.logger.debug(f'sourceItem = {self.sourceItem.text(0) if self.sourceItem else None}, targetItem = {self.targetItem.text(0) if self.targetItem else None}')
        super().dragLeaveEvent(event)

    def dragMoveEvent(self, event):
        """Surcharge de la méthode de déplacement d'un item
        Args:
            event (QMouseEvent): Événement de mouvement de la souris
        """
        # self.logger.info(f"event={event}")
        self.targetItem = self.itemAt(event.position().toPoint())
        if not self.targetItem:
            event.ignore()
            self.logger.debug(f"Aucun item sous le curseur.")
            return
        
        if self.targetItem.itemType == "cnx":
            target_rect = self.visualItemRect(self.targetItem)
            half_height = target_rect.height() // 2
            top_zone = target_rect.adjusted(0, 0, 0, -half_height)
            bottom_zone = target_rect.adjusted(0, half_height, 0, 0)
            current_pos = event.position().toPoint()

            if top_zone.contains(current_pos):
                # self.logger.debug(f"Drop autorisé au-dessus de '{self.targetItem.text(0)}'")
                event.accept()
            elif bottom_zone.contains(current_pos):
                # self.logger.debug(f"Drop autorisé en dessous de '{self.targetItem.text(0)}'")
                event.accept()
            else:
                self.logger.info(f"Drop interdit sur '{self.targetItem.text(0)}'")
                event.ignore()
        else:
            self.logger.info(f"Drop autorisé sur '{self.targetItem.text(0)}'")
            event.accept()
        super().dragMoveEvent(event)

    def dropEvent(self, event):
        """Surcharge de la méthode de drop d'un item pour gérer le déplacement d'un item dans l'arborescence
        Args:
            event (QMouseEvent): Événement de drop
        """
        # self.logger.info(f"event={event}")
        self.logger.debug(f"Déplacement de '{self.sourceItem.text(0)}' vers '{self.targetItem.text(0)}' en cours...")
        self.logger.debug(f"sourceItem.itemType='{self.sourceItem.itemType}', targetItem.itemType='{self.targetItem.itemType}'")
        if self.sourceItem is None or self.targetItem is None:
            self.logger.debug(f"Drop annulé : sourceItem ou targetItem est None (sourceItem='{self.sourceItem.text(0) if self.sourceItem else None}', targetItem='{self.targetItem.text(0) if self.targetItem else None}').")
            return
        if self.sourceItem == self.targetItem:
            self.logger.debug(f"Drop annulé : sourceItem et targetItem sont identiques (sourceItem='{self.sourceItem.text(0) if self.sourceItem else None}', targetItem='{self.targetItem.text(0) if self.targetItem else None}').")
            return
        if self.targetItem.itemType == "cnx":
            if self.targetItem and self.sourceItem:
                target_rect = self.visualItemRect(self.targetItem)
                half_height = target_rect.height() // 2
                top_zone = target_rect.adjusted(0, 0, 0, -half_height)
                bottom_zone = target_rect.adjusted(0, half_height, 0, 0)
                current_pos = event.position().toPoint()
                self.logger.debug(f"targetItem='{self.targetItem.text(0)}', target_rect={target_rect}, top_zone={top_zone}, bottom_zone={bottom_zone}, current_pos={current_pos}")
                
                if top_zone.contains(current_pos):
                    self.logger.debug(f"Insertion de '{self.sourceItem.text(0)}' au-dessus de '{self.targetItem.text(0)}'")
                    self.insert_item_above(self.targetItem, self.sourceItem)
                elif bottom_zone.contains(current_pos):
                    self.logger.debug(f"Insertion de '{self.sourceItem.text(0)}' en dessous de '{self.targetItem.text(0)}'")
                    self.insert_item_below(self.targetItem, self.sourceItem)
                else:
                    self.logger.debug("Drop annulé : zone non autorisée.")
                    return
        else:
            super().dropEvent(event)  # Appelle le comportement par défaut

        self.sourceItem = None
        self.targetItem = None
        self.logger.debug(f"Purge de sourceItem (='{self.sourceItem}'), targetItem (='{self.targetItem}').")
        self.logger.debug("Drop effectué.")
        self.yarcom.update_connexions_after_drop()

    def insert_item_above(self, target_item, source_item):
        """Insère source_item au-dessus de target_item dans l'arborescence
        Args:
            target_item (QTreeWidgetItem): L'item cible au-dessus duquel insérer
            source_item (QTreeWidgetItem): L'item à insérer
        """
        target_parent = target_item.parent() or self.invisibleRootItem()
        target_row = target_parent.indexOfChild(target_item)
        source_parent = source_item.parent() or self.invisibleRootItem()
        source_row = source_parent.indexOfChild(source_item)
        source_parent.takeChild(source_row)
        target_parent.insertChild(target_row, source_item)

    def insert_item_below(self, target_item, source_item):
        """Insère source_item en dessous de target_item dans l'arborescence
        Args:
            target_item (QTreeWidgetItem): L'item cible en dessous duquel insérer
            source_item (QTreeWidgetItem): L'item à insérer
        """
        target_parent = target_item.parent() or self.invisibleRootItem()
        source_parent = source_item.parent() or self.invisibleRootItem()
        source_row = source_parent.indexOfChild(source_item)
        source_parent.takeChild(source_row)
        target_row = target_parent.indexOfChild(target_item)
        target_parent.insertChild(target_row + 1, source_item)

class YARCOM(QMainWindow, Ui_MainWindow, QObject):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Affiche la barre de menu dans la fenêtre (et non en natif sur macOS)
        self.menuBar().setNativeMenuBar(False)

        # Logging stuf
        self.logger = logging.getLogger(self.__class__.__name__)

        # Variables diverses
        self.version = "0.1"
        self.version_string = "2024/11/13"
        self.author = "faro"
        self.confFile = "yarcom.qt.conf.orig.json"
        self.kbdxPassword = False
        self.passwordCiphered = False
        self.kbdxDialogAlreadyShown = False
        self.globalConf = dict()
        self.connexions = dict()
        self.apps = dict()
        self.last_query = None
        self.search_results = []
        self.search_index = -1
        self.selected_item = None
        self.tw_Cnx = CustomQTreeWidget(self)
        self.tw_Cnx.setHeaderHidden(True)

        # Retirer self.tw_Cnx de son emplacement actuel
        if self.tw_Cnx.parent():
            self.tw_Cnx.setParent(None)

        # Ajouter self.tw_Cnx dans gb_Tree entre hl_TreeButtons et hl_ToggleTree
        self.gb_Tree.layout().insertWidget(
            self.gb_Tree.layout().indexOf(self.hl_ToggleTree), self.tw_Cnx
        )

        self.setWindowTitle("YARCoM for Qt")
        self.conf = self.readConfFile(self.confFile)
        if self.conf is None:
            self.displayError("Fichier de configuration absent ou invalide.")
            return
        self.globalConf = self.conf.get("global", {})
        self.connexions = self.conf.get("connexions", {})
        self.apps = self.globalConf.get("apps", {})

        self.parseConf()
        self.logger.debug(f"conf :\n{json.dumps(self.conf, indent=4)}")
        self.logger.debug(f"globalConf :\n{json.dumps(self.globalConf, indent=4)}")
        self.logger.debug(f"connexions :\n{json.dumps(self.connexions, indent=4)}")
        self.logger.debug(f"apps :\n{json.dumps(self.apps, indent=4)}")
        self.populate_twCnx(self.connexions)
        self.displayPasswordDialog()

        # Connecter les signaux de sélection
        self.tw_Cnx.itemClicked.connect(self.on_twCnx_itemClicked)
        self.tw_Cnx.itemDoubleClicked.connect(self.on_twCnx_itemDoubleClicked)
        self.pb_ModifyCnx.clicked.connect(self.on_pb_ModifyCnx_clicked)
        self.le_Search.returnPressed.connect(self.on_search_enter)
        self.pb_FoldUnfoldTree.clicked.connect(self.on_pb_FoldUnfoldTree_clicked)
        self.pb_TreeAddSection.clicked.connect(self.on_pb_TreeAddSection_clicked)
        self.pb_TreeAddCnx.clicked.connect(self.on_pb_TreeAddCnx_clicked)
        self.pb_TreeDelete.clicked.connect(self.on_pb_TreeDelete_clicked)
        self.pb_Preferences.clicked.connect(self.on_pb_Preferences_clicked)
        self.tw_Cnx.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_Cnx.customContextMenuRequested.connect(self.show_context_menu)

        if self.cb_Application is not None:
            self.cb_Application.addItems(self.apps.keys())
            self.cb_Application.setCurrentIndex(-1)
            self.cb_Application.setEnabled(False)
        if self.cb_KBDX is not None:
            self.cb_KBDX.addItems(self.globalConf.get("kbdxFiles", {}).keys())
            self.cb_KBDX.setCurrentIndex(-1)
            self.cb_KBDX.setEnabled(False)
        # Désactiver et effacer les champs de modification par défaut
        self.clear_twCnx_fields()

    def update_connexions_after_drop(self):
        """Met à jour le dictionnaire des connexions après un déplacement d'item dans l'arborescence"""
        self.connexions.clear()
        self.topTreeWidgetItems_to_dict()
        self.write_to_file(self.conf, self.confFile)

    def show_context_menu(self, position):
        """Affiche le menu contextuel
        Args:
            position (QPoint): Position du curseur en pixels obtenue lors du signal.
        """
        # Récupère l'élément sous le curseur
        item = self.tw_Cnx.itemAt(position)
        if item is None:
            return

        if item.itemType == "branche":
            self.display_item(item)
        elif item.itemType == "cnx":
            self.display_item(item)

        # Création du menu contextuel
        menu = QMenu()
        apps_list = list()
        if item.itemType == "cnx":
            for k in self.apps.keys():
                apps_list.append(menu.addAction(k))

        # Exécution de l'action sélectionnée
        action = menu.exec(self.tw_Cnx.viewport().mapToGlobal(position))
        if action in apps_list:
            app_name = action.text()
            self.logger.info(f"Lancement de l'application '{app_name}' pour la connexion '{item.text(0)}'")
            # Ici, ajouter le code pour lancer l'application avec les paramètres de la connexion
            self.run_command(item, app_name)

    def save_expansion_state(self):
        """Sauvegarde l'état d'expansion de l'arborescence"""
        def recursive_save(item):
            state = {"expanded": item.isExpanded(), "children": {}}
            for i in range(item.childCount()):
                child = item.child(i)
                state["children"][child.text(0)] = recursive_save(child)
            return state

        expansion_state = {}
        for i in range(self.tw_Cnx.topLevelItemCount()):
            top_item = self.tw_Cnx.topLevelItem(i)
            expansion_state[top_item.text(0)] = recursive_save(top_item)
        return expansion_state

    def restore_expansion_state(self, expansion_state):
        """Restaure l'état d'expansion de l'arborescence"""
        def recursive_restore(item, state):
            if state.get("expanded", False):
                item.setExpanded(True)
            else:
                item.setExpanded(False)
            for i in range(item.childCount()):
                child = item.child(i)
                child_state = state["children"].get(child.text(0), {})
                recursive_restore(child, child_state)

        for i in range(self.tw_Cnx.topLevelItemCount()):
            top_item = self.tw_Cnx.topLevelItem(i)
            if top_item.text(0) in expansion_state:
                recursive_restore(top_item, expansion_state[top_item.text(0)])

    def on_pb_Preferences_clicked(self):
        """Ouvre la boîte de dialogue des préférences KeePass"""
        self.displayPreferenceDialog()
        for kbdx_name, kbdx_info in self.globalConf.get("kbdxFiles", {}).items():
            self.logger.debug(f"{kbdx_name} : {json.dumps(kbdx_info, indent=4)}")
            ciphered = kbdx_info.get("ciphered", False)
            valid = kbdx_info.get("valid", False)
            if ciphered is False or valid is False:
                self.logger.debug(f"  - Affichage de la boîte de dialogue de mot de passe pour '{kbdx_name}'")
                self.displayPasswordDialog(kbdx_name)
        if self.cb_Application.count() != len(list(self.globalConf["apps"].keys())):
            self.apps = self.globalConf.get("apps", {})
            self.cb_Application.clear()
            self.cb_Application.addItems(self.apps.keys())
            self.cb_Application.setCurrentIndex(-1)
            self.cb_Application.setEnabled(False)
        if self.cb_KBDX.count() != len(list(self.globalConf["kbdxFiles"].keys())):
            self.cb_KBDX.clear()
            self.cb_KBDX.addItems(self.globalConf.get("kbdxFiles", {}).keys())
            self.cb_KBDX.setCurrentIndex(-1)
            self.cb_KBDX.setEnabled(False)

    def on_pb_TreeDelete_clicked(self):
        """Supprime l'item de l'arborescence"""

        item = self.selected_item
        if item is None:
            self.displayError(f"Aucune sélection.", is_error=True, auto_close=True)
            return

        # Sauvegarder l'état d'expansion de l'arborescence
        expansion_state = self.save_expansion_state()

        # Créer une boîte de dialogue de confirmation
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Demande de confirmation")
        message_box.setText(f"Voulez-vous vraiment supprimer l'item '{item.text(0)}' ?")
        message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        message_box.setButtonText(QMessageBox.Yes, "Oui")  # Modifier le texte du bouton "Yes"
        message_box.setButtonText(QMessageBox.No, "Non")  # Modifier le texte du bouton "No"
        message_box.setDefaultButton(QMessageBox.No)

        # Afficher la boîte de dialogue
        reply = message_box.exec_()
        # Traiter la réponse de l'utilisateur
        if reply != QMessageBox.Yes:
            self.logger.debug(f"Suppression de '{self.selected_item.text(0)}' annulée.")
            return
        self.logger.debug(f"Suppression de '{self.selected_item.text(0)}' confirmée.")

        # Supprimer l'item de l'arborescence QTreeWidgetItem
        parent = item.parent()
        if parent:
            index = parent.indexOfChild(item)
            parent.takeChild(index)
        else:
            index = self.tw_Cnx.indexOfTopLevelItem(item)
            self.tw_Cnx.takeTopLevelItem(index)
            parent = self.tw_Cnx

        # Sauvegarder les modifications dans le fichier de configuration
        self.connexions.clear()
        self.topTreeWidgetItems_to_dict()
        self.write_to_file(self.conf, self.confFile)
        self.reload_tree(expansion_state)

    def on_pb_TreeAddCnx_clicked(self):
        """Ajoute une connexion dans l'arborescence"""

        if self.selected_item is not None:
            parent = self.tw_Cnx.currentItem()
        else:
            parent = self.tw_Cnx
        new_list = list()
        current_counter = None
        highest_counter = None

        if parent != self.tw_Cnx:
            if parent.itemType == "cnx":
                self.displayError(f"'{parent.text(0)}' est une connexion.", is_error=True, auto_close=True)
                return

        cnx_name = "Nouvelle connexion"

        # Vérifier si la connexion existe déjà
        if parent is self.tw_Cnx:
            for i in range(self.tw_Cnx.topLevelItemCount()):
                match = re.match(rf'{cnx_name}(\s+\((\d+)\))?', self.tw_Cnx.topLevelItem(i).text(0))
                if match:
                    new_list.append(self.tw_Cnx.topLevelItem(i).text(0))
                    current_counter = int(match.group(2)) if match.group(2) else None
                    if highest_counter is None or current_counter > highest_counter:
                        highest_counter = current_counter if current_counter else 0
        else:
            for i in range(parent.childCount()):
                match = re.match(rf'{cnx_name}(\s+\((\d+)\))?', parent.child(i).text(0))
                if match:
                    new_list.append(parent.child(i).text(0))
                    current_counter = int(match.group(2)) if match.group(2) else None
                    if highest_counter is None or current_counter > highest_counter:
                        highest_counter = current_counter if current_counter else 0

        if highest_counter is not None:
            next_counter = highest_counter + 1
            cnx_name = f'{cnx_name} ({next_counter})'

        # Ajouter la nouvelle connexion dans l'arborescence
        new_item = CustomQTreeWidgetItem([cnx_name], itemType = "cnx", itemCnx = {"ip":'', "port":'', "user":'', "app":'', "kbdx":''})
        if parent is self.tw_Cnx:
            parent.addTopLevelItem(new_item)
        else:
            parent.addChild(new_item)

        # Sauvegarder les modifications dans le fichier de configuration
        self.connexions.clear()
        self.topTreeWidgetItems_to_dict()
        self.write_to_file(self.conf, self.confFile)

    def on_pb_TreeAddSection_clicked(self):
        """Ajoute une section (branche) dans l'arborescence"""

        if self.selected_item is not None:
            parent = self.tw_Cnx.currentItem()
        else:
            parent = self.tw_Cnx
        new_list = list()
        current_counter = None
        highest_counter = None

        if parent != self.tw_Cnx:
            if parent.itemType == "cnx":
                self.displayError(f"'{parent.text(0)}' est une connexion.", is_error=True, auto_close=True)
                return

        section_name = "Nouvelle section"

        # Vérifier si la section existe déjà
        if parent is self.tw_Cnx:
            for i in range(self.tw_Cnx.topLevelItemCount()):
                match = re.match(rf'{section_name}(\s+\((\d+)\))?', self.tw_Cnx.topLevelItem(i).text(0))
                if match:
                    new_list.append(self.tw_Cnx.topLevelItem(i).text(0))
                    current_counter = int(match.group(2)) if match.group(2) else None
                    if highest_counter is None or current_counter > highest_counter:
                        highest_counter = current_counter if current_counter else 0
        else:
            for i in range(parent.childCount()):
                match = re.match(rf'{section_name}(\s+\((\d+)\))?', parent.child(i).text(0))
                if match:
                    new_list.append(parent.child(i).text(0))
                    current_counter = int(match.group(2)) if match.group(2) else None
                    if highest_counter is None or current_counter > highest_counter:
                        highest_counter = current_counter if current_counter else 0

        if highest_counter is not None:
            next_counter = highest_counter + 1
            section_name = f'{section_name} ({next_counter})'

        # Ajouter la nouvelle section dans l'arborescence
        new_item = CustomQTreeWidgetItem([section_name], itemType="branche")
        if parent is self.tw_Cnx:
            parent.addTopLevelItem(new_item)
        else:
            parent.addChild(new_item)

        # Sauvegarder les modifications dans le fichier de configuration
        self.connexions.clear()
        self.topTreeWidgetItems_to_dict()
        # self.conf = self.reload_conf()
        self.write_to_file(self.conf, self.confFile)

    def clear_twCnx_fields(self):
        """Désactive et efface les champs de modification de la connexion sélectionnée"""
        if self.le_IP is not None:
            self.le_IP.setEnabled(False)
            self.le_IP.clear()
        if self.le_Port is not None:
            self.le_Port.setEnabled(False)
            self.le_Port.clear()
        if self.le_User is not None:
            self.le_User.setEnabled(False)
            self.le_User.clear()
        if self.le_Hostname is not None:
            self.le_Hostname.setEnabled(False)
            self.le_Hostname.clear()
        # Désactiver le bouton de sauvegarde par défaut
        if self.pb_ModifyCnx is not None:
            self.pb_ModifyCnx.setEnabled(False)

    def on_twCnx_itemDoubleClicked(self, item):
        """Lance l'application par défaut de la connexion sélectionnée
        Args:
            item (CustomQTreeWidgetItem): L'item double-cliqué dans l'arborescence
        """
        # Vérifier si c'est une connexion
        if item.itemType == "branche":
            self.displayError("Sélectionnez une connexion valide.", auto_close=True)
            return
        self.run_command(item, "default")
        
    def run_command(self, item, application="default"):
        """Lance l'application par défaut de la connexion sélectionnée
        Args:
            item (CustomQTreeWidgetItem): L'item double-cliqué dans l'arborescence
            application (str): L'application à exécuter :
                "default" : lance l'application par défaut de la connexion
                "custom" : lance l'application spécifiée dans le menu contextuel
        """
        if application == "default":
            # Récupérer l'app par défaut de la connexion
            app_name = item.itemCnx.get("app", "")
        else:
            # Récupérer l'app spécifiée dans le menu contextuel
            app_name = application
        
        app_conf = self.globalConf.get("apps", {}).get(app_name, {})
        app_bin = app_conf.get("bin", "")
        app_args = app_conf.get("args", "")
        
        user = item.itemCnx.get("user", "")
        ip = item.itemCnx.get("ip", "")
        if application == "default":
            port = item.itemCnx.get("port", "")
        else:
            port = app_conf.get("port", "")
        kbdx = item.itemCnx.get("kbdx", "")

        if not app_bin or not ip:
            self.displayError("Impossible de lancer l'application : configuration incomplète.", auto_close=True)
            return
        self.logger.debug(f"app_name={app_name},\napp_bin={app_bin},\napp_args={app_args},\nuser={user},\nip={ip},\nport={port},\nkbdx={kbdx}")

        # Vérifier si le(s) mot(s) de passe KeePass a/ont été saisi(s)
        if kbdx and not self.globalConf["kbdxFiles"][kbdx]["ciphered"]:
            self.displayPasswordDialog()
            if not self.globalConf["kbdxFiles"][kbdx]["ciphered"] and not self.globalConf["kbdxFiles"][kbdx]["valid"]:
                self.displayError(f"Impossible de lancer l'application : mot de passe KeePass pour '{kbdx}' non saisi.", delay=5000, auto_close=True)
                return

        # Rechercher le compte dans la base KeePass si kbdx et user sont définis
        self.logger.info(f"Recherche du compte '{user}' dans la base KeePass '{kbdx}'")
        account_info = self.search_account_in_vault(kbdx, user)
        if account_info:
            accountDatas = json.dumps(account_info, indent=4)
            accountDatas = re.sub(r'("password"\s*:\s*").*(")', r'\1********\2', accountDatas)
            self.logger.debug(f"  - account_info   : {accountDatas}")
        else:
            self.logger.info(f"Compte introuvable dans la base KeePass '{kbdx}'")

        # Création de la commande à lancer
        cmd = list()
        my_args = list()
        if app_bin:
            cmd.extend(app_bin.split())
        for part in app_args.split():
            part = part.replace("<user>", user).replace("<ip>", ip).replace("<port>", port).replace("<password>", account_info.get("password", ""))
            my_args.append(part)
        cmd.append(' '.join(my_args))
        cmdStringProtected = ' '.join(cmd).replace(account_info.get("password", ""), "********") if account_info.get("password", "") else ' '.join(cmd)
        self.logger.debug(f"Lancement de : {cmdStringProtected}")
        account_info.clear()  # Effacer les informations sensibles de la mémoire
        ##################################################################################
        # if sys.platform.startswith('win'):
        #     # Sous Windows, utiliser shell=True pour permettre l'expansion des variables d'environnement et l'exécution de commandes internes
        #     shell = False
        # else:
        #     # Sous Linux/Mac, cmd doit être une liste d'arguments et shell=False pour éviter les problèmes de sécurité
        #     shell = False
        #     if "ssh" in app_bin.lower() or "ssh" in app_args.lower():
        #         # Si l'application est SSH, utiliser shell=True pour permettre l'expansion des variables d'environnement et l'exécution de commandes internes
        #         shell = True
        ##################################################################################

        try:
            subprocess.Popen(cmd, shell=False)
        except Exception as e:
            self.displayError(f"Erreur lors du lancement : {e}", delay=2000, auto_close=True)
        except FileNotFoundError:
            print("Commande introuvable")
        except subprocess.TimeoutExpired:
            print("Temps d'attente dépassé")

    def on_pb_FoldUnfoldTree_clicked(self):
        """Plie ou déplie toute l'arborescence selon l'état actuel"""
        any_expanded = False
        for i in range(self.tw_Cnx.topLevelItemCount()):
            item = self.tw_Cnx.topLevelItem(i)
            if item.isExpanded():
                any_expanded = True
                break
        if any_expanded:
            for i in range(self.tw_Cnx.topLevelItemCount()):
                item = self.tw_Cnx.topLevelItem(i)
                self._toggle_item_recursive(item, expand=False)
        else:
            for i in range(self.tw_Cnx.topLevelItemCount()):
                item = self.tw_Cnx.topLevelItem(i)
                self._toggle_item_recursive(item, expand=True)

    def _toggle_item_recursive(self, item, expand):
        """Plie ou déplie récursivement un item et ses enfants"""
        item.setExpanded(expand)
        for j in range(item.childCount()):
            self._toggle_item_recursive(item.child(j), expand)

    def on_search_enter(self):
        """Recherche et sélectionne les items correspondants à la recherche"""
        query = self.le_Search.text().strip().lower()
        if not query:
            self.search_results = []
            self.search_index = -1
            return
        
        # Si la requête a changé, lancer une nouvelle requête
        if self.last_query is None or self.last_query != query:
            self.last_query = query
            self.search_results = []
            self.search_index = 0
        
            self.search_item(self.tw_Cnx)
        
            if len(self.search_results) > 0:
                item = self.search_results[0]
                if len(self.search_results) > 1:
                    self.search_index = 1
                self.tw_Cnx.setCurrentItem(item)
                self.display_item(item)
            else:
                self.displayError("Aucune correspondance trouvée.", auto_close=True)
        else:
            # Même requête, passer au résultat suivant
            if self.search_results:
                item = self.search_results[self.search_index]
                self.tw_Cnx.setCurrentItem(item)
                self.display_item(item)
                self.search_index += 1
                if self.search_index >= len(self.search_results):
                    self.search_index = 0
    
    def search_item(self, parent):
        """Recherche itérative parmi les QTreeWidgetItem

        Args:
            parent (QTreeWidgetItem): parent des items balayés par la recherche
        """
        motif = re.compile(rf'{self.last_query}')
        if parent == self.tw_Cnx:
            for i in range(parent.topLevelItemCount()):
                item = parent.topLevelItem(i)
                result = motif.search(item.text(0).lower())
                if result:
                    self.search_results.append(item)
                if item.itemType == "branche":
                    self.search_item(item)
                elif item.itemType == "cnx":
                    for k,v in item.itemCnx.items():
                        result_k = motif.search(k)
                        result_v = motif.search(v)
                        if result_k or result_v:
                            if item not in self.search_results:
                                self.search_results.append(item)
        else:
            for i in range(parent.childCount()):
                item = parent.child(i)
                result = motif.search(item.text(0).lower())
                if result:
                    self.search_results.append(item)
                if item.itemType == "branche":
                    self.search_item(item)
                elif item.itemType == "cnx":
                    for k,v in item.itemCnx.items():
                        result_k = motif.search(k)
                        result_v = motif.search(v)
                        if result_k or result_v:
                            if item not in self.search_results:
                                self.search_results.append(item)

    def on_pb_ModifyCnx_clicked(self):
        """Sauvegarde les modifications des champs de la connexion sélectionnée si au moins une valeur a changé"""
        item = self.tw_Cnx.currentItem()
        if item is None:
            self.displayError("Aucune élément sélectionnée.\n Veuillez une branche ou une connexion dans l'arborescence.", delay=5000, auto_close=True)
            return

        # Sauvegarder l'état d'expansion de l'arborescence
        expansion_state = self.save_expansion_state()

        # Initialiser les variables
        changed = False
        new_values = {}
        # Récupérer les nouvelles valeurs si c'est une connexion ou une branche
        if item.itemType == "cnx":
            new_values = {
                "ip": self.le_IP.text(),
                "port": self.le_Port.text(),
                "user": self.le_User.text(),
                "hostname": self.le_Hostname.text(),
                "app": self.cb_Application.currentText() if self.cb_Application.currentText() else "",
                "kbdx": self.cb_KBDX.currentText() if self.cb_KBDX.currentText() else ""
            }
            # Vérifier si une valeur a changé
            if self.le_Hostname.text() != item.text(0):
                changed = True
            else:
                for k, v in new_values.items():
                    if item.itemCnx.get(k, "") != v and k not in ["hostname"]:
                        changed = True
                        break
        elif item.itemType == "branche":
            new_values = {
                "hostname": self.le_Hostname.text()
            }
            # Vérifier si la valeur a changé
            if item.text(0) != new_values["hostname"]:
                changed = True

        if not changed:
            self.displayError("Aucune modification détectée.", auto_close=True)
            return

        # Mettre à jour les valeurs
        self.logger.debug(f"Modification de la connexion '{item.text(0)}'")
        self.logger.debug(f"\tnouvelles valeurs :{json.dumps(new_values, indent=4)}")
        if item.itemType == "cnx":
            for k, v in new_values.items():
                if k == "hostname":
                    item.setText(0, new_values[k])
                else:
                    item.itemCnx[k] = new_values[k]
        elif item.itemType == "branche":
            item.setText(0, new_values["hostname"])

        self.connexions.clear()
        self.topTreeWidgetItems_to_dict()
        self.write_to_file(self.conf, self.confFile)
        self.reload_tree(expansion_state)

    def topTreeWidgetItems_to_dict(self):
        """Convertit les QTreeWidgetItem de niveau supérieur en dictionnaire"""
        for i in range(self.tw_Cnx.topLevelItemCount()):
            top_item = self.tw_Cnx.topLevelItem(i)
            self.logger.debug(f"{i}: {top_item.text(0)}")
            if top_item.itemType == "branche":
                self.connexions[top_item.text(0)] = dict()
                self.childTreeWidgetItems_to_dict(top_item, self.connexions[top_item.text(0)])
            elif top_item.itemType == "cnx":
                self.connexions[top_item.text(0)] = top_item.itemCnx

    def childTreeWidgetItems_to_dict(self, item, current_dict_branch):
        """Convertit les QTreeWidgetItem enfants en dictionnaire
        Args:
            item (QTreeWidgetItem): item parent
            current_dict_branch (dict): dictionnaire de la branche courante
        """
        for i in range(item.childCount()):
            child = item.child(i)
            self.logger.debug(f"{i}: {child.text(0)}")
            if child.itemType == "branche":
                current_dict_branch[child.text(0)] = dict()
                self.childTreeWidgetItems_to_dict(child, current_dict_branch[child.text(0)])
            elif child.itemType == "cnx":
                current_dict_branch[child.text(0)] = child.itemCnx

    def reload_conf(self):
        """Recharge la configuration à partir du fichier de configuration"""
        try:
            with open(self.confFile, "r", encoding="utf-8") as f:
                conf = json.load(f)
            conf["connexions"] = self.connexions
            # self.write_to_file(conf, self.confFile)
        except Exception as e:
            self.displayError(f"Erreur lors de la sauvegarde : {e}")
        return conf

    def reload_tree(self, expansion_state):
        """Recharge l'arborescence et restaure l'état d'expansion
        Args:
            expansion_state (dict): état d'expansion de l'arborescence
        """
        if self.connexions:
            # Recharger l'arborescence
            self.tw_Cnx.clear()
            self.populate_twCnx(self.connexions)
            self.selected_item = None

            # Restaurer l'état d'expansion de l'arborescence
            self.restore_expansion_state(expansion_state)

            # Réinitialiser les champs
            self.cb_Application.setCurrentIndex(-1)
            self.cb_KBDX.setCurrentIndex(-1)
            self.clear_twCnx_fields()

    def write_to_file(self, conf, source_file):
        """Écrit la configuration dans le fichier source
        Args:
            conf (dict): configuration à écrire
            source_file (str): chemin du fichier source
        """
        new_conf = deepcopy(conf)

        if "kbdxFiles" in new_conf.get("global", {}):
            new_conf["global"]["kbdx"] = dict()
            for kbdx_name in self.globalConf.get("kbdxFiles", {}).keys():
                new_conf["global"]["kbdx"][kbdx_name] = self.globalConf["kbdxFiles"][kbdx_name]["file"]
            del new_conf["global"]["kbdxFiles"]
        self.logger.debug(f'new_conf={json.dumps(new_conf, indent=4)}')
        
        with open(source_file, "w", encoding="utf-8") as f:
            json.dump(new_conf, f, indent=4)
        self.logger.debug(f"Modifications sauvegardées dans {source_file}")
        # self.displayError("Modifications sauvegardées avec succès.", is_error=False, auto_close=True)
        return True

    def on_twCnx_itemClicked(self, item):
        """Affiche les infos de l'item sélectionné dans l'arborescence

        Args:
            item (QTreeWidgetItem): item sélectionné
        Returns:
        """
        # Vérifier si l'item est déjà sélectionné
        if item.isSelected() and self.selected_item == item:
            self.logger.debug(f"Désélection de l'item '{item.text(0)}'")
            self.tw_Cnx.clearSelection()  # Désélectionner l'item
            item.setSelected(False)
            # item.setExpanded(not item.isExpanded())
            self.selected_item = None
            self.logger.debug(f'item.isSelected()={item.isSelected()}, self.selected_item={self.selected_item}, self.tw_Cnx.currentItem()={self.tw_Cnx.currentItem()}')
            # Réinitialiser les champs
            self.cb_Application.setCurrentIndex(-1)
            self.cb_KBDX.setCurrentIndex(-1)
            self.clear_twCnx_fields()
            return
        else:
            self.selected_item = item  # Mettre à jour l'item sélectionné
            self.logger.debug(f"Sélection de l'item '{item.text(0)}'")
            # Plier/Déplier l'item si c'est une branche
            if item.itemType == "branche":
                item.setExpanded(True)

        if item.itemType == "branche":
            self.display_item(item)
            return
        elif item.itemType == "cnx":
            self.display_item(item)

    def display_item(self, item):
        """Affiche les informations de l'item sélectionné dans les champs
        Args:
            item (QTreeWidgetItem): item à afficher
        """
        if item.itemType == "branche":
            # Réinitialiser les champs
            self.cb_Application.setCurrentIndex(-1)
            self.cb_KBDX.setCurrentIndex(-1)
            self.clear_twCnx_fields()
            self.logger.debug(f"Name='{item.text(0)}', itemType='{item.itemType}', itemCnx='{item.itemCnx}'")
            # Activer le champ de nom de section
            self.le_Hostname.setEnabled(True)
            self.pb_ModifyCnx.setEnabled(True)
            # Masquer les champs de connexion
            self.lb_IP.hide()
            self.le_IP.hide()
            self.lb_Port.hide()
            self.le_Port.hide()
            self.lb_User.hide()
            self.le_User.hide()
            self.lb_App.hide()
            self.cb_Application.hide()
            self.lb_KBDX.hide()
            self.cb_KBDX.hide()
            # Afficher le champ de nom de section
            if item.text(0) is not None:
                    self.lb_Hostname.setText("Nom de la section :")
                    self.le_Hostname.setText(item.text(0))
        elif item.itemType == "cnx":
            # Réinitialiser les champs
            self.cb_Application.setCurrentIndex(-1)
            self.cb_KBDX.setCurrentIndex(-1)
            self.le_IP.clear()
            self.le_Port.clear()
            self.le_User.clear()
            self.le_Hostname.clear()
            self.lb_Hostname.setText("Nom d'hôte")
            # Afficher les champs de connexion
            self.lb_IP.show()
            self.le_IP.show()
            self.lb_Port.show()
            self.le_Port.show()
            self.lb_User.show()
            self.le_User.show()
            self.lb_App.show()
            self.cb_Application.show()
            self.lb_KBDX.show()
            self.cb_KBDX.show()
            # Récupérer les clefs et valeurs
            keys = list(item.itemCnx.keys())
            if ("ip" or "port" or "app" or "kbdx" or "user") in keys:
                self.logger.debug(f"{item.text(0)}={json.dumps(item.itemCnx, indent=4)}")
                for k in keys:
                    if self.le_IP is not None and k == "ip":
                        self.le_IP.setText(item.itemCnx[k])
                    if self.le_Port is not None and k == "port":
                        self.le_Port.setText(str(item.itemCnx[k]))
                    if self.le_User is not None and k == "user":
                        self.le_User.setText(item.itemCnx[k])
                    if self.le_Hostname is not None:
                        self.le_Hostname.setText(item.text(0))
                    if self.cb_Application is not None and k == "app":
                        index = self.cb_Application.findText(item.itemCnx[k])
                        if index != -1:
                            self.cb_Application.setCurrentIndex(index)
                        else:
                            self.cb_Application.setCurrentIndex(-1)
                    if self.cb_KBDX is not None and k == "kbdx":
                        index = self.cb_KBDX.findText(item.itemCnx[k])
                        if index != -1:
                            self.cb_KBDX.setCurrentIndex(index)
                        else:
                            self.cb_KBDX.setCurrentIndex(-1)
                # Activer les champs de modification
                self.le_IP.setEnabled(True)
                self.le_Port.setEnabled(True)
                self.le_User.setEnabled(True)
                self.le_Hostname.setEnabled(True)
                self.cb_Application.setEnabled(True)
                self.cb_KBDX.setEnabled(True)
                self.pb_ModifyCnx.setEnabled(True)
            else:
                self.logger.debug(f"L'item '{item.text(0)}' ne contient pas de connexion directe : {json.dumps(item.itemCnx, indent=4)}")
                self.cb_Application.setCurrentIndex(-1)
                self.cb_KBDX.setCurrentIndex(-1)
                self.clear_twCnx_fields()

    def populate_twCnx(self, data, parent=None):
        """Remplie l'arborescence avec les données des connexions

        Args:
            data (dict): données de connexions du fichier de configuration
        """
        self.logger.debug(f"data={data}, parent={parent}")
        connexion_keys = {"ip", "port", "user", "app", "kbdx"}

        if parent is None:
            parent = self.tw_Cnx
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    if connexion_keys.issubset(v.keys()):
                        self.logger.debug(f'{k} est un connexion ({v}).')
                        item = CustomQTreeWidgetItem([str(k)], itemType="cnx", itemCnx=v)
                        item.setFlags(item.flags() | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
                        parent.addTopLevelItem(item) if parent is self.tw_Cnx else parent.addChild(item)
                    else:
                        self.logger.debug(f'{k} est une branche.')
                        item = CustomQTreeWidgetItem([str(k)], itemType="branche")
                        item.setFlags(item.flags() | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled)
                        parent.addTopLevelItem(item) if parent is self.tw_Cnx else parent.addChild(item)
                        self.populate_twCnx(v, item)

    def displayPreferenceDialog(self):
        """Affiche la boîte de dialogue des préférences KeePass"""
        if not hasattr(self, "prefForm"):
            self.prefForm = Preferences_Dialog(self.globalConf)
        self.prefForm.setWindowTitle("Préférences")
        self.prefForm.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)
        self.prefForm.setModal(True)
        self.logger.debug(f"self.conf = {json.dumps(self.conf, indent=4)}")
        self.prefForm.exec()
        if self.prefForm.prefs_modified:
            self.logger.debug("Modifications des préférences sauvegardées.")
            self.logger.debug(f"self.new_conf = {json.dumps(self.conf, indent=4)}")
            self.write_to_file(self.conf, self.confFile)
        else:
            self.logger.debug("Aucune modification des préférences détectée.")

    def displayPasswordDialog(self, kbdx_name=None):
        """Créé et affiche la boîte de dialogue de saisie des mots de passe KeePass
        Args:
            kbdx_name (str, optional): nom du coffre KeePass pour lequel le mot de passe doit être saisi. Si None, tous les coffres sont traités.
        """
        status_kbdxForm = None
        if self.kbdxPassword:
            kbdxFiles = self.globalConf.get("kbdxFiles", {})
            nb_kbdxFiles = len(kbdxFiles)
            kbdxTitle = "Saisie des mots de passes KeePass" if nb_kbdxFiles > 1 else "Saisie du mot de passe KeePass"
            gbTitle = "Liste des coffre-forts KeePass" if nb_kbdxFiles > 1 else "Coffre-fort KeePass"

            self.logger.debug(f"self.kbdxPassword = {self.kbdxPassword}")
            self.logger.debug(f"kbdxFiles = {list(kbdxFiles.keys())}")
            self.logger.debug(f"nb_kbdxFiles = {nb_kbdxFiles}")
            if not self.kbdxDialogAlreadyShown and not hasattr(self, "kbdxForm"):
                self.kbdxForm = KBDX_Dialog(kbdxFiles)
            else:
                self.kbdxForm.updateKbdxFiles(kbdxFiles)
            self.kbdxForm.setWindowTitle(kbdxTitle)
            self.kbdxForm.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)
            self.kbdxForm.groupBox.setTitle(gbTitle)

            self.logger.debug(f"self.kbdxDialogAlreadyShown = {self.kbdxDialogAlreadyShown}")
            if not self.kbdxDialogAlreadyShown:
                self.kbdxForm.setModal(True)
                self.kbdxDialogAlreadyShown = True
            else:
                self.kbdxForm.setModal(False)
            self.logger.debug(f"self.kbdxDialogAlreadyShown = {self.kbdxDialogAlreadyShown}")

            while any(not kbdxFiles[vault]["valid"] for vault in kbdxFiles):
                status_kbdxForm = self.kbdxForm.exec()
                if status_kbdxForm == 1:
                    self.logger.debug("Saisie de(s) mot(s) de passe sélectionnée.")
                    for vault in kbdxFiles.keys():
                        if kbdxFiles[vault]["ciphered"] is False and kbdxFiles[vault]["valid"] is False:
                            self.logger.debug(f"Traitement de '{vault}'")
                            kbdxFiles[vault]["ciphered"] = self.kbdxForm.cipherPassword(vault)
                            self.logger.debug(f"kbdxFiles[{vault}] = {json.dumps(kbdxFiles[vault], indent=4)}")
                            if kbdxFiles[vault]["ciphered"]:
                                file = kbdxFiles[vault].get("file", "")
                                self.logger.debug(f"{vault} keepass key  = {kbdxFiles[vault].get("password", "")} ({self.kbdxForm.uncipherPassword(kbdxFiles[vault].get("password", "")) if kbdxFiles[vault].get("password", "") else ''})")
                                kbdxFiles[vault]["valid"] = self.kbdxForm.openKbdxFile(vault, file)
                                if kbdxFiles[vault]["valid"] is False:
                                    kbdxFiles[vault]["ciphered"] = False
                                    kbdxFiles[vault]["password"] = ""
                                    self.logger.debug(f"Réinitialisation de kbdxFiles[{vault}] = {kbdxFiles[vault]}")
                                else:
                                    self.logger.debug(f"Ouverture de '{file}' pour '{vault}' réussie.")
                            else:
                                self.logger.debug(f"Mot de passe pour '{vault}' non chiffré.")
                elif status_kbdxForm == 0:
                    self.logger.debug("Saisie de(s) mot(s) de passe abandonnée.")
                    break
            self.logger.debug(f"self.conf = {json.dumps(self.conf, indent=4)}")

    def search_account_in_vault(self, vault, account_name):
        """Recherche un compte dans la base KeePass spécifiée par vault
        Args:
            vault (str): nom du coffre KeePass
            account_name (str): nom du compte à rechercher
        Returns:
            dict: informations du compte si trouvé, sinon None
        """
        kbdxFiles = self.globalConf.get("kbdxFiles", {})
        if vault not in kbdxFiles:
            self.logger.error(f"Coffre KeePass '{vault}' non trouvé.")
            self.displayError(f"Coffre KeePass '{vault}' non trouvé.")
            return None
        file_path = kbdxFiles[vault].get("file", "")
        password = kbdxFiles[vault].get("password", "")
        if kbdxFiles[vault]["ciphered"] and kbdxFiles[vault]["valid"]:
            password = self.kbdxForm.uncipherPassword(password)
        result = self.kbdxForm.search_account(file_path, password, account_name)
        return result

    def readConfFile(self, confFile):
        """Lire le fichier de configuration
        Args:
            confFile (JSON file): fichier contenant les parties globales et de connexion
        Returns:
            dict: configuration
        """
        self.logger.debug(f"confFile = {confFile}")
        try:
            with open(confFile, "r", encoding="utf-8") as conf:
                conf = json.load(conf)
            return conf
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Erreur : {e}")
            return None

    def parseConf(self):
        """Analyse et modifie la configuration chargée"""
        # Vérifier les fichiers de base de données KeePass dbx, puis définir kdbxPassword sur True
        kbdxPasswords = dict()
        kbdxFiles = self.globalConf.get("kbdx", None)
        if kbdxFiles is not None:
            self.logger.debug(f"kbdxFiles={kbdxFiles}")
            index = 0
            for k,v in kbdxFiles.items():
                thisFile = Path(v)
                if thisFile.exists():
                    if thisFile.is_file():
                        kbdxPasswords[k]=dict()
                        kbdxPasswords[k]["file"] = v
                        kbdxPasswords[k]["password"] = ""
                        kbdxPasswords[k]["ciphered"] = False
                        kbdxPasswords[k]["valid"] = False
                        kbdxPasswords[k]["index"] = index
                        index += 1
                    else:
                        self.logger.error(f"{thisFile} n'est pas un fichier.")
                        self.displayError(f"{thisFile} n'est pas un fichier")
                else:
                    self.logger.error(f"{thisFile} n'existe pas.")
                    self.displayError(f"{thisFile} n'existe pas")

            self.logger.debug(f"new kbdxFiles={kbdxPasswords}")
            # Replace kbdx sub-dict from conf with kbdxPasswords
            if "kbdx" in self.globalConf:
                del self.globalConf["kbdx"]
            self.globalConf["kbdxFiles"] = kbdxPasswords
            if bool(self.globalConf["kbdxFiles"]):
                self.kbdxPassword = True

    def displayError(self, error, is_error = True, delay=5000, auto_close=False):
        """Affiche une boîte de dialogue d'erreur ou passage d'information

        Args:
            error (str): Le message d'erreur ou d'information à afficher.
            is_error (bool, optionel): Indique si le message est une erreur, sinon c'est une information. Par défaut à True.
            delay (int, optionel): Le délai en millisecondes avant de fermer automatiquement la boîte de dialogue. Par défaut à 5000.
            auto_close (bool, optionel): Indique si la boîte de dialogue doit se fermer automatiquement. Par défaut à False.
        """
        errorBox = QMessageBox()
        errorBox.setIcon(QMessageBox.Critical)
        if is_error:
            errorBox.setIcon(QMessageBox.Critical)
            errorBox.setWindowTitle("Erreur")
            errorBox.setText(f"L'erreur suivante est survenue :\n {error}")
        else:
            errorBox.setIcon(QMessageBox.Information)
            errorBox.setWindowTitle("Information")
            errorBox.setText(f"L'évènement suivant est survenu :\n {error}")
            errorBox.setStandardButtons(QMessageBox.Ok)
        if auto_close:
            errorBox.setStandardButtons(QMessageBox.NoButton)  # Pas de bouton OK
        else:
            errorBox.setStandardButtons(QMessageBox.Ok)
        errorBox.show()
        if auto_close:
            QTimer.singleShot(delay, lambda: setattr(self, "_errorBox", None))
        self._errorBox = errorBox # Keep a reference to prevent garbage collection


if __name__ == "__main__":
    yarcom = QApplication(sys.argv)
    window = YARCOM()
    window.show()

    sys.exit(yarcom.exec())