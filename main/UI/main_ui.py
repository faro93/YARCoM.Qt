# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGridLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QVBoxLayout, QWidget)
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(320, 862)
        MainWindow.setMinimumSize(QSize(180, 600))
        MainWindow.setMaximumSize(QSize(320, 16777215))
        icon = QIcon()
        icon.addFile(u":/main/YARCoM.icon.340x225.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.action_Save = QAction(MainWindow)
        self.action_Save.setObjectName(u"action_Save")
        self.actionSave_as = QAction(MainWindow)
        self.actionSave_as.setObjectName(u"actionSave_as")
        self.actionSave_as.setEnabled(False)
        self.action_Close = QAction(MainWindow)
        self.action_Close.setObjectName(u"action_Close")
        self.action_Preferences = QAction(MainWindow)
        self.action_Preferences.setObjectName(u"action_Preferences")
        self.action_Quit = QAction(MainWindow)
        self.action_Quit.setObjectName(u"action_Quit")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gb_Tree = QGroupBox(self.centralwidget)
        self.gb_Tree.setObjectName(u"gb_Tree")
        self.gb_Tree.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.gb_Tree.setFlat(False)
        self.gb_Tree.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.gb_Tree)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.hl_TreeButtons = QHBoxLayout()
        self.hl_TreeButtons.setObjectName(u"hl_TreeButtons")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_TreeButtons.addItem(self.horizontalSpacer_5)

        self.pb_TreeAddSection = QPushButton(self.gb_Tree)
        self.pb_TreeAddSection.setObjectName(u"pb_TreeAddSection")
        icon1 = QIcon()
        icon1.addFile(u":/main/add_folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_TreeAddSection.setIcon(icon1)
        self.pb_TreeAddSection.setIconSize(QSize(32, 32))

        self.hl_TreeButtons.addWidget(self.pb_TreeAddSection)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_TreeButtons.addItem(self.horizontalSpacer_3)

        self.pb_TreeAddCnx = QPushButton(self.gb_Tree)
        self.pb_TreeAddCnx.setObjectName(u"pb_TreeAddCnx")
        icon2 = QIcon()
        icon2.addFile(u":/main/add_computer.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_TreeAddCnx.setIcon(icon2)
        self.pb_TreeAddCnx.setIconSize(QSize(32, 32))

        self.hl_TreeButtons.addWidget(self.pb_TreeAddCnx)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_TreeButtons.addItem(self.horizontalSpacer_4)

        self.pb_TreeDelete = QPushButton(self.gb_Tree)
        self.pb_TreeDelete.setObjectName(u"pb_TreeDelete")
        icon3 = QIcon()
        icon3.addFile(u":/main/trash.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_TreeDelete.setIcon(icon3)
        self.pb_TreeDelete.setIconSize(QSize(32, 32))

        self.hl_TreeButtons.addWidget(self.pb_TreeDelete)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_TreeButtons.addItem(self.horizontalSpacer_6)

        self.pb_Preferences = QPushButton(self.gb_Tree)
        self.pb_Preferences.setObjectName(u"pb_Preferences")
        icon4 = QIcon()
        icon4.addFile(u":/main/prefs.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_Preferences.setIcon(icon4)
        self.pb_Preferences.setIconSize(QSize(32, 32))

        self.hl_TreeButtons.addWidget(self.pb_Preferences)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_TreeButtons.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.hl_TreeButtons)

        self.hl_ToggleTree = QHBoxLayout()
        self.hl_ToggleTree.setObjectName(u"hl_ToggleTree")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_ToggleTree.addItem(self.horizontalSpacer_9)

        self.pb_FoldUnfoldTree = QPushButton(self.gb_Tree)
        self.pb_FoldUnfoldTree.setObjectName(u"pb_FoldUnfoldTree")

        self.hl_ToggleTree.addWidget(self.pb_FoldUnfoldTree)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hl_ToggleTree.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.hl_ToggleTree)

        self.fl_TreeSearch = QFormLayout()
        self.fl_TreeSearch.setObjectName(u"fl_TreeSearch")
        self.lb_Search = QLabel(self.gb_Tree)
        self.lb_Search.setObjectName(u"lb_Search")
        self.lb_Search.setText(u"Rechercher")

        self.fl_TreeSearch.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lb_Search)

        self.le_Search = QLineEdit(self.gb_Tree)
        self.le_Search.setObjectName(u"le_Search")

        self.fl_TreeSearch.setWidget(0, QFormLayout.ItemRole.FieldRole, self.le_Search)


        self.verticalLayout.addLayout(self.fl_TreeSearch)


        self.verticalLayout_3.addWidget(self.gb_Tree)

        self.gb_Detail = QGroupBox(self.centralwidget)
        self.gb_Detail.setObjectName(u"gb_Detail")
        self.gb_Detail.setEnabled(True)
        self.gb_Detail.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.verticalLayout_2 = QVBoxLayout(self.gb_Detail)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.fl_Detail = QFormLayout()
        self.fl_Detail.setObjectName(u"fl_Detail")
        self.lb_Hostname = QLabel(self.gb_Detail)
        self.lb_Hostname.setObjectName(u"lb_Hostname")

        self.fl_Detail.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lb_Hostname)

        self.le_Hostname = QLineEdit(self.gb_Detail)
        self.le_Hostname.setObjectName(u"le_Hostname")

        self.fl_Detail.setWidget(0, QFormLayout.ItemRole.FieldRole, self.le_Hostname)

        self.lb_IP = QLabel(self.gb_Detail)
        self.lb_IP.setObjectName(u"lb_IP")

        self.fl_Detail.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lb_IP)

        self.le_IP = QLineEdit(self.gb_Detail)
        self.le_IP.setObjectName(u"le_IP")

        self.fl_Detail.setWidget(1, QFormLayout.ItemRole.FieldRole, self.le_IP)

        self.lb_Port = QLabel(self.gb_Detail)
        self.lb_Port.setObjectName(u"lb_Port")

        self.fl_Detail.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lb_Port)

        self.le_Port = QLineEdit(self.gb_Detail)
        self.le_Port.setObjectName(u"le_Port")

        self.fl_Detail.setWidget(2, QFormLayout.ItemRole.FieldRole, self.le_Port)

        self.lb_App = QLabel(self.gb_Detail)
        self.lb_App.setObjectName(u"lb_App")

        self.fl_Detail.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lb_App)

        self.cb_Application = QComboBox(self.gb_Detail)
        self.cb_Application.setObjectName(u"cb_Application")

        self.fl_Detail.setWidget(3, QFormLayout.ItemRole.FieldRole, self.cb_Application)

        self.lb_KBDX = QLabel(self.gb_Detail)
        self.lb_KBDX.setObjectName(u"lb_KBDX")

        self.fl_Detail.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lb_KBDX)

        self.cb_KBDX = QComboBox(self.gb_Detail)
        self.cb_KBDX.setObjectName(u"cb_KBDX")

        self.fl_Detail.setWidget(4, QFormLayout.ItemRole.FieldRole, self.cb_KBDX)

        self.lb_User = QLabel(self.gb_Detail)
        self.lb_User.setObjectName(u"lb_User")

        self.fl_Detail.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lb_User)

        self.le_User = QLineEdit(self.gb_Detail)
        self.le_User.setObjectName(u"le_User")

        self.fl_Detail.setWidget(5, QFormLayout.ItemRole.FieldRole, self.le_User)


        self.verticalLayout_2.addLayout(self.fl_Detail)

        self.gl_DetailButtons = QGridLayout()
        self.gl_DetailButtons.setObjectName(u"gl_DetailButtons")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_DetailButtons.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.pb_ModifyCnx = QPushButton(self.gb_Detail)
        self.pb_ModifyCnx.setObjectName(u"pb_ModifyCnx")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_ModifyCnx.sizePolicy().hasHeightForWidth())
        self.pb_ModifyCnx.setSizePolicy(sizePolicy)
        icon5 = QIcon()
        icon5.addFile(u":/main/edit.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pb_ModifyCnx.setIcon(icon5)
        self.pb_ModifyCnx.setIconSize(QSize(32, 32))

        self.gl_DetailButtons.addWidget(self.pb_ModifyCnx, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gl_DetailButtons.addItem(self.horizontalSpacer_2, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gl_DetailButtons)


        self.verticalLayout_3.addWidget(self.gb_Detail)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QRect(0, 0, 320, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Ouvrir", None))
        self.actionOpen.setIconText(QCoreApplication.translate("MainWindow", u"Ouvrir", None))
#if QT_CONFIG(tooltip)
        self.actionOpen.setToolTip(QCoreApplication.translate("MainWindow", u"Ouvrir", None))
#endif // QT_CONFIG(tooltip)
        self.action_Save.setText(QCoreApplication.translate("MainWindow", u"Enregistrer", None))
        self.actionSave_as.setText(QCoreApplication.translate("MainWindow", u"Enregistrer sous", None))
        self.action_Close.setText(QCoreApplication.translate("MainWindow", u"Fermer", None))
        self.action_Preferences.setText(QCoreApplication.translate("MainWindow", u"Pr\u00e9f\u00e9rences", None))
        self.action_Quit.setText(QCoreApplication.translate("MainWindow", u"&Quitter", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"A propos", None))
        self.gb_Tree.setTitle(QCoreApplication.translate("MainWindow", u"Liste des connexions", None))
#if QT_CONFIG(tooltip)
        self.pb_TreeAddSection.setToolTip(QCoreApplication.translate("MainWindow", u"Ajouter une section", None))
#endif // QT_CONFIG(tooltip)
        self.pb_TreeAddSection.setText("")
#if QT_CONFIG(tooltip)
        self.pb_TreeAddCnx.setToolTip(QCoreApplication.translate("MainWindow", u"Ajouter une connexion", None))
#endif // QT_CONFIG(tooltip)
        self.pb_TreeAddCnx.setText("")
#if QT_CONFIG(shortcut)
        self.pb_TreeAddCnx.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.pb_TreeDelete.setToolTip(QCoreApplication.translate("MainWindow", u"Supprimer l'objet", None))
#endif // QT_CONFIG(tooltip)
        self.pb_TreeDelete.setText("")
#if QT_CONFIG(tooltip)
        self.pb_Preferences.setToolTip(QCoreApplication.translate("MainWindow", u"Pr\u00e9f\u00e9rences", None))
#endif // QT_CONFIG(tooltip)
        self.pb_Preferences.setText("")
        self.pb_FoldUnfoldTree.setText(QCoreApplication.translate("MainWindow", u"Plier/D\u00e9plier", None))
        self.gb_Detail.setTitle(QCoreApplication.translate("MainWindow", u"Detail de la connexion", None))
        self.lb_Hostname.setText(QCoreApplication.translate("MainWindow", u"Nom d'h\u00f4te", None))
        self.lb_IP.setText(QCoreApplication.translate("MainWindow", u"Adresse IP", None))
        self.lb_Port.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.lb_App.setText(QCoreApplication.translate("MainWindow", u"Application", None))
        self.lb_KBDX.setText(QCoreApplication.translate("MainWindow", u"Coffre KeePass", None))
        self.lb_User.setText(QCoreApplication.translate("MainWindow", u"Utilisateur", None))
#if QT_CONFIG(tooltip)
        self.pb_ModifyCnx.setToolTip(QCoreApplication.translate("MainWindow", u"Modifier la connexion", None))
#endif // QT_CONFIG(tooltip)
        self.pb_ModifyCnx.setText("")
    # retranslateUi

