# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preferences.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QTabWidget, QTableView,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(665, 390)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_Apps = QWidget()
        self.tab_Apps.setObjectName(u"tab_Apps")
        self.verticalLayout_5 = QVBoxLayout(self.tab_Apps)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.tab_Apps)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tv_apps = QTableView(self.groupBox)
        self.tv_apps.setObjectName(u"tv_apps")

        self.verticalLayout_3.addWidget(self.tv_apps)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_Apps)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lb_appsname = QLabel(self.groupBox_2)
        self.lb_appsname.setObjectName(u"lb_appsname")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lb_appsname)

        self.le_appsname = QLineEdit(self.groupBox_2)
        self.le_appsname.setObjectName(u"le_appsname")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.le_appsname)

        self.lb_appspath = QLabel(self.groupBox_2)
        self.lb_appspath.setObjectName(u"lb_appspath")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lb_appspath)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.le_appspath = QLineEdit(self.groupBox_2)
        self.le_appspath.setObjectName(u"le_appspath")

        self.horizontalLayout_2.addWidget(self.le_appspath)

        self.pb_appspath = QPushButton(self.groupBox_2)
        self.pb_appspath.setObjectName(u"pb_appspath")

        self.horizontalLayout_2.addWidget(self.pb_appspath)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.lb_appsargs = QLabel(self.groupBox_2)
        self.lb_appsargs.setObjectName(u"lb_appsargs")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lb_appsargs)

        self.le_appsargs = QLineEdit(self.groupBox_2)
        self.le_appsargs.setObjectName(u"le_appsargs")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.le_appsargs)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_appsadd = QPushButton(self.groupBox_2)
        self.pb_appsadd.setObjectName(u"pb_appsadd")

        self.horizontalLayout.addWidget(self.pb_appsadd)

        self.pb_appsdel = QPushButton(self.groupBox_2)
        self.pb_appsdel.setObjectName(u"pb_appsdel")

        self.horizontalLayout.addWidget(self.pb_appsdel)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addWidget(self.groupBox_2)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.tab_Apps, "")
        self.tab_Kbdx = QWidget()
        self.tab_Kbdx.setObjectName(u"tab_Kbdx")
        self.verticalLayout_6 = QVBoxLayout(self.tab_Kbdx)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_3 = QGroupBox(self.tab_Kbdx)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tv_kbdx = QTableView(self.groupBox_3)
        self.tv_kbdx.setObjectName(u"tv_kbdx")

        self.verticalLayout_7.addWidget(self.tv_kbdx)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tab_Kbdx)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.lb_kbdxname = QLabel(self.groupBox_4)
        self.lb_kbdxname.setObjectName(u"lb_kbdxname")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lb_kbdxname)

        self.le_kbdxname = QLineEdit(self.groupBox_4)
        self.le_kbdxname.setObjectName(u"le_kbdxname")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.le_kbdxname)

        self.lb_kbdxpath = QLabel(self.groupBox_4)
        self.lb_kbdxpath.setObjectName(u"lb_kbdxpath")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lb_kbdxpath)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.le_kbdxpath = QLineEdit(self.groupBox_4)
        self.le_kbdxpath.setObjectName(u"le_kbdxpath")

        self.horizontalLayout_3.addWidget(self.le_kbdxpath)

        self.pb_kbdxpath = QPushButton(self.groupBox_4)
        self.pb_kbdxpath.setObjectName(u"pb_kbdxpath")

        self.horizontalLayout_3.addWidget(self.pb_kbdxpath)


        self.formLayout_2.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_3)


        self.verticalLayout_8.addLayout(self.formLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pb_kbdxadd = QPushButton(self.groupBox_4)
        self.pb_kbdxadd.setObjectName(u"pb_kbdxadd")

        self.horizontalLayout_4.addWidget(self.pb_kbdxadd)

        self.pb_kbdxdel = QPushButton(self.groupBox_4)
        self.pb_kbdxdel.setObjectName(u"pb_kbdxdel")

        self.horizontalLayout_4.addWidget(self.pb_kbdxdel)


        self.verticalLayout_8.addLayout(self.horizontalLayout_4)


        self.verticalLayout_6.addWidget(self.groupBox_4)

        self.tabWidget.addTab(self.tab_Kbdx, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Dialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Liste des applications", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Nouvelle application", None))
        self.lb_appsname.setText(QCoreApplication.translate("Dialog", u"Nom", None))
        self.lb_appspath.setText(QCoreApplication.translate("Dialog", u"Chemin", None))
        self.pb_appspath.setText(QCoreApplication.translate("Dialog", u"Rechercher", None))
        self.lb_appsargs.setText(QCoreApplication.translate("Dialog", u"Arguments", None))
        self.pb_appsadd.setText(QCoreApplication.translate("Dialog", u"Ajouter", None))
        self.pb_appsdel.setText(QCoreApplication.translate("Dialog", u"Supprimer", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Apps), QCoreApplication.translate("Dialog", u"Applications", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Liste des coffre-forts KeePass", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Nouveau coffre-fort", None))
        self.lb_kbdxname.setText(QCoreApplication.translate("Dialog", u"Nom", None))
        self.lb_kbdxpath.setText(QCoreApplication.translate("Dialog", u"Chemin", None))
        self.pb_kbdxpath.setText(QCoreApplication.translate("Dialog", u"Rechercher", None))
        self.pb_kbdxadd.setText(QCoreApplication.translate("Dialog", u"Ajouter", None))
        self.pb_kbdxdel.setText(QCoreApplication.translate("Dialog", u"Supprimer", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Kbdx), QCoreApplication.translate("Dialog", u"Coffre-forts KeePass", None))
    # retranslateUi

