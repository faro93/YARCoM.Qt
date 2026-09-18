# import sys
import logging
# import json
# from cryptography.fernet import Fernet
# from pykeepass import PyKeePass

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout
from PySide6.QtGui import QStandardItemModel, QStandardItem
from about.UI.about_ui import Ui_Dialog

class About_Dialog(QDialog, Ui_Dialog):
    def __init__(self, author="faro", version="", description="", license="GPLv3", website="https://github.com/faro93/YARCoM.Qt"):
        super().__init__()
        self.setupUi(self)
        
        # Logging stuf
        self.logger = logging.getLogger(self.__class__.__name__)
        # self.logger.setLevel(logging.DEBUG)
        
        self.lb_author.setText(f"Auteur : {author}")
        self.lb_version.setText(f"Version : {version}")
        self.lb_description.setText(f"Description : {description}")
        self.lb_license.setText(f"Licence : {license}")
        # self.lb_website.setText(f"Site web : {website}")
