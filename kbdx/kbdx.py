import sys
import logging
from cryptography.fernet import Fernet
from pykeepass import PyKeePass
import base64

from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtWidgets import QDialog, QApplication, QLabel, QFormLayout, QLineEdit, QMessageBox
from kbdx.UI.kbdx_ui import Ui_Dialog

class KBDX_Dialog(QDialog, Ui_Dialog):
    def __init__(self, kbdxFiles):
        super().__init__()
        self.setupUi(self)

        # Logging stuf
        self.logger = logging.getLogger(self.__class__.__name__)

        # Variables diverses
        self.kbdxFiles = kbdxFiles
        self.lb_KBDX = list()
        self.le_KBDX = list()
        self.cipher = self.setCipher()
        self.kps = list()
        self.cancelSelected = False
        
        self.logger.debug(f"self.kbdxFiles = {list(self.kbdxFiles.keys())}")
        self.createForm()

    def createForm(self):
        """Créer dynamiquement le formulaire en fonction du nombre de coffres KeePass"""
        for index, vault in enumerate(list(self.kbdxFiles.keys())):
            self.logger.debug(f"self.kbdxFiles['{vault}']:{self.kbdxFiles[vault]}")
            setattr(self, f"lb_KBDX{index}", QLabel(self.groupBox))
            self.lb_KBDX.append(getattr(self, f'lb_KBDX{index}'))
            self.lb_KBDX[index].setObjectName(f"lb_KBDX{index}")
            self.formLayout.setWidget(index, QFormLayout.LabelRole, self.lb_KBDX[index])
            setattr(self, f"le_KBDX{index}", QLineEdit(self.groupBox))
            self.le_KBDX.append(getattr(self, f'le_KBDX{index}'))
            self.formLayout.setWidget(index, QFormLayout.FieldRole, self.le_KBDX[index])
            self.lb_KBDX[index].setText(f"{vault}")
            self.le_KBDX[index].setPlaceholderText(f"Saisir le mot de passe pour '{vault}'")
            self.le_KBDX[index].setEchoMode(QLineEdit.Password)
        self.pb_OK.clicked.connect(self.accept)
        self.pb_Cancel.clicked.connect(self.reject)

    def cipherPassword(self, vault):
        """Chiffre le mot de passe pour un coffre donné"""
        index = self.kbdxFiles[vault]['index']
        encrypted_password = self.cipher.encrypt(self.le_KBDX[index].text().encode())
        # Convertir en base64 pour une meilleure compatibilité
        if isinstance(encrypted_password, bytes):
            self.logger.debug(f"encrypted_password (bytes) = {encrypted_password}")
            encrypted_password = base64.b64encode(encrypted_password).decode('utf-8')
            self.kbdxFiles[vault]['password'] = encrypted_password
        self.logger.debug(f"self.kbdxFiles['{vault}']['password']:'{self.kbdxFiles[vault]['password']}, type={type(self.kbdxFiles[vault]['password'])}'")
        self.logger.debug(f"self.kbdxFiles['{vault}']['ciphered']:'{self.kbdxFiles[vault]['ciphered']}'")
        return True

    def uncipherPassword(self, password):
        """Déchiffre le mot de passe pour un coffre donné"""
        if isinstance(password, str):
            password = base64.b64decode(password.encode('utf-8'))
        return self.cipher.decrypt(password).decode()
    
    def setCipher(self):
        """Configure la clef de chiffrement"""
        return Fernet(Fernet.generate_key())

    def openKbdxFile(self, vault, filename):
        """Ouvre le fichier KeePass avec le mot de passe saisi"""
        try:
            result = PyKeePass(filename, password=self.uncipherPassword(self.kbdxFiles[vault]["password"]))
            self.kps.append(result)
            self.logger.info(f"Coffre-fort {vault} ({filename}) est ouvert avec succès.")
            
        except Exception as e:
            self.logger.error(f"Une erreur est survenue : {e}")
            self.displayError(vault, e)
            return False
        self.logger.debug(f"self.kps = {self.kps}")
        return True
    
    def updateKbdxFiles(self, kbdxFiles):
        """Met à jour la liste des coffres KeePass dans le formulaire"""
        self.kbdxFiles = kbdxFiles
        for index, vault in enumerate(list(self.kbdxFiles.keys())):
            self.logger.debug(f"updateKbdxFiles - vault: {vault}, index: {index}")
            if index < len(self.lb_KBDX):
                self.lb_KBDX[index].setText(f"{vault}")
                self.le_KBDX[index].setPlaceholderText(f"Saisir le mot de passe pour '{vault}'")
            else:
                setattr(self, f"lb_KBDX{index}", QLabel(self.groupBox))
                self.lb_KBDX.append(getattr(self, f'lb_KBDX{index}'))
                self.lb_KBDX[index].setObjectName(f"lb_KBDX{index}")
                self.formLayout.setWidget(index, QFormLayout.LabelRole, self.lb_KBDX[index])
                setattr(self, f"le_KBDX{index}", QLineEdit(self.groupBox))
                self.le_KBDX.append(getattr(self, f'le_KBDX{index}'))
                self.formLayout.setWidget(index, QFormLayout.FieldRole, self.le_KBDX[index])
                self.lb_KBDX[index].setText(f"{vault}")
                self.le_KBDX[index].setPlaceholderText(f"Saisir le mot de passe pour '{vault}'")
                self.le_KBDX[index].setEchoMode(QLineEdit.Password)
        # Masquer les champs supplémentaires s'il y en a
        for index in range(len(self.kbdxFiles), len(self.lb_KBDX)):
            self.lb_KBDX[index].deleteLater()
            self.le_KBDX[index].deleteLater()
    
    # def onCancel(self):
    #     self.cancelSelected = True
    
    def search_account(self, filename, password, account_name):
        """Ouvre la base KeePass et cherche un compte par titre ou nom d'utilisateur"""
        try:
            kp = PyKeePass(filename, password=password)
            # Recherche par titre
            entry = kp.find_entries(title=account_name, first=True)
            if entry:
                return {
                    "title": entry.title,
                    "username": entry.username,
                    "password": entry.password,
                    "url": entry.url,
                    "notes": entry.notes
                }
            # Recherche par nom d'utilisateur
            entry = kp.find_entries(username=account_name, first=True)
            if entry:
                return {
                    "title": entry.title,
                    "username": entry.username,
                    "password": entry.password,
                    "url": entry.url,
                    "notes": entry.notes
                }
            return None
        except Exception as e:
            self.logger.error(f"Erreur lors de la recherche dans {filename} : {e}")
            return None
    
    def displayError(self, vault, error):
        """Affiche une boîte de dialogue d'erreur spécifique à un coffre"""
        errorBox = QMessageBox()
        errorBox.setIcon(QMessageBox.Critical)
        errorBox.setWindowTitle(f"Erreur pour le coffre '{vault}'")
        errorBox.setText(f"L'erreur suivante est survenue pour le coffre '{vault}' :\n {error}")
        errorBox.setStandardButtons(QMessageBox.Ok)
        errorBox.exec()

if __name__ == "__main__":
    kbdx = QApplication(sys.argv)
    window = KBDX_Dialog()
    window.show()
    
    sys.exit(kbdx.exec_())
    