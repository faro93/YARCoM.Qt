# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QSizePolicy, QSpacerItem, QWidget)
import Ressources_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 332)
        icon = QIcon()
        icon.addFile(u":/main/icons/YARCoM.icon.340x225.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        Dialog.setWindowIcon(icon)
        self.gridLayout_4 = QGridLayout(Dialog)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lb_logo = QLabel(Dialog)
        self.lb_logo.setObjectName(u"lb_logo")
        self.lb_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lb_logo, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_3, 0, 0, 1, 1)

        self.lb_version = QLabel(Dialog)
        self.lb_version.setObjectName(u"lb_version")

        self.gridLayout.addWidget(self.lb_version, 0, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.lb_description = QLabel(Dialog)
        self.lb_description.setObjectName(u"lb_description")

        self.gridLayout.addWidget(self.lb_description, 0, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_4, 1, 0, 1, 1)

        self.lb_author = QLabel(Dialog)
        self.lb_author.setObjectName(u"lb_author")

        self.gridLayout.addWidget(self.lb_author, 1, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.lb_license = QLabel(Dialog)
        self.lb_license.setObjectName(u"lb_license")

        self.gridLayout.addWidget(self.lb_license, 1, 3, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 1, 4, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.lb_website = QLabel(Dialog)
        self.lb_website.setObjectName(u"lb_website")
        self.lb_website.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lb_website, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lb_logo.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><img src=\":/main/icons/YARCoM.by.faro340x233.png\"/></p></body></html>", None))
        self.lb_version.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.lb_description.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.lb_author.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.lb_license.setText(QCoreApplication.translate("Dialog", u"TextLabel", None))
        self.lb_website.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><a href=\"https://github.com/faro93/YARCoM.Qt\"><span style=\" text-decoration: underline; color:#c4c6ca;\">Lien Github</span></a></p></body></html>", None))
    # retranslateUi

