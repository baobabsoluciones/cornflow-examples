# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(578, 697)
        self.actionOpen_from = QAction(MainWindow)
        self.actionOpen_from.setObjectName(u"actionOpen_from")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setSizeConstraint(QLayout.SetNoConstraint)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Config = QWidget()
        self.Config.setObjectName(u"Config")
        self.horizontalLayout_4 = QHBoxLayout(self.Config)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.chooseFile = QPushButton(self.Config)
        self.chooseFile.setObjectName(u"chooseFile")

        self.horizontalLayout_2.addWidget(self.chooseFile)

        self.file_path = QLabel(self.Config)
        self.file_path.setObjectName(u"file_path")
        self.file_path.setMinimumSize(QSize(300, 0))
        self.file_path.setBaseSize(QSize(0, 0))
        self.file_path.setTextInteractionFlags(Qt.LinksAccessibleByMouse|Qt.TextEditable)

        self.horizontalLayout_2.addWidget(self.file_path)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.loginCheck = QLabel(self.Config)
        self.loginCheck.setObjectName(u"loginCheck")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.loginCheck.setFont(font)
        self.loginCheck.setStyleSheet(u"QLabel { color : red; }")

        self.verticalLayout_2.addWidget(self.loginCheck)

        self.instCheck = QLabel(self.Config)
        self.instCheck.setObjectName(u"instCheck")
        self.instCheck.setFont(font)
        self.instCheck.setStyleSheet(u"QLabel { color : red; }")
        self.instCheck.setTextFormat(Qt.AutoText)

        self.verticalLayout_2.addWidget(self.instCheck)

        self.solCheck = QLabel(self.Config)
        self.solCheck.setObjectName(u"solCheck")
        self.solCheck.setFont(font)
        self.solCheck.setStyleSheet(u"QLabel { color : red; }")

        self.verticalLayout_2.addWidget(self.solCheck)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(-1, 5, -1, 5)
        self.label_222 = QLabel(self.Config)
        self.label_222.setObjectName(u"label_222")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_222)

        self.server = QLineEdit(self.Config)
        self.server.setObjectName(u"server")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.server)

        self.label = QLabel(self.Config)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.username = QLineEdit(self.Config)
        self.username.setObjectName(u"username")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.username)

        self.label_2 = QLabel(self.Config)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.password = QLineEdit(self.Config)
        self.password.setObjectName(u"password")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.password)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 5, -1, 5)
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.login = QPushButton(self.Config)
        self.login.setObjectName(u"login")

        self.horizontalLayout_8.addWidget(self.login)

        self.signup = QPushButton(self.Config)
        self.signup.setObjectName(u"signup")

        self.horizontalLayout_8.addWidget(self.signup)

        self.logout = QPushButton(self.Config)
        self.logout.setObjectName(u"logout")

        self.horizontalLayout_8.addWidget(self.logout)

        self.checkBoxDebug = QCheckBox(self.Config)
        self.checkBoxDebug.setObjectName(u"checkBoxDebug")

        self.horizontalLayout_8.addWidget(self.checkBoxDebug)


        self.verticalLayout.addLayout(self.horizontalLayout_8)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.get_instances = QPushButton(self.Config)
        self.get_instances.setObjectName(u"get_instances")

        self.horizontalLayout.addWidget(self.get_instances)

        self.send_instance = QPushButton(self.Config)
        self.send_instance.setObjectName(u"send_instance")

        self.horizontalLayout.addWidget(self.send_instance)


        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.instances = QListView(self.Config)
        self.instances.setObjectName(u"instances")
        self.instances.setContextMenuPolicy(Qt.ActionsContextMenu)

        self.verticalLayout_5.addWidget(self.instances)


        self.verticalLayout.addLayout(self.verticalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(-1, 5, -1, 5)
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setContentsMargins(-1, 5, -1, 5)
        self.label_3 = QLabel(self.Config)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.maxTime = QLineEdit(self.Config)
        self.maxTime.setObjectName(u"maxTime")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.maxTime)

        self.label_4 = QLabel(self.Config)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.solver = QComboBox(self.Config)
        self.solver.setObjectName(u"solver")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.solver)


        self.horizontalLayout_6.addLayout(self.formLayout_2)

        self.solve_instance = QPushButton(self.Config)
        self.solve_instance.setObjectName(u"solve_instance")

        self.horizontalLayout_6.addWidget(self.solve_instance)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.executions = QListView(self.Config)
        self.executions.setObjectName(u"executions")

        self.verticalLayout_6.addWidget(self.executions)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.get_results = QPushButton(self.Config)
        self.get_results.setObjectName(u"get_results")

        self.horizontalLayout_5.addWidget(self.get_results)

        self.show_solution = QPushButton(self.Config)
        self.show_solution.setObjectName(u"show_solution")

        self.horizontalLayout_5.addWidget(self.show_solution)

        self.showLog = QPushButton(self.Config)
        self.showLog.setObjectName(u"showLog")

        self.horizontalLayout_5.addWidget(self.showLog)

        self.exportLog = QPushButton(self.Config)
        self.exportLog.setObjectName(u"exportLog")

        self.horizontalLayout_5.addWidget(self.exportLog)


        self.verticalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.verticalLayout_6)


        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.tabWidget.addTab(self.Config, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 578, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen_from)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.chooseFile.setDefault(False)
        self.send_instance.setDefault(False)
        self.solve_instance.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"El Baile", None))
        self.actionOpen_from.setText(QCoreApplication.translate("MainWindow", u"Open from...", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Export As...", None))
#if QT_CONFIG(tooltip)
        self.Config.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>configuration</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.chooseFile.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.file_path.setText("")
        self.loginCheck.setText(QCoreApplication.translate("MainWindow", u"Logged-out", None))
        self.instCheck.setText(QCoreApplication.translate("MainWindow", u"No instance loaded", None))
        self.solCheck.setText(QCoreApplication.translate("MainWindow", u"No solution loaded", None))
        self.label_222.setText(QCoreApplication.translate("MainWindow", u"Server", None))
        self.server.setText(QCoreApplication.translate("MainWindow", u"http://localhost:5000", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.username.setText(QCoreApplication.translate("MainWindow", u"some_email@gmail.com", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.password.setText(QCoreApplication.translate("MainWindow", u"some_password", None))
        self.login.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.signup.setText(QCoreApplication.translate("MainWindow", u"Signup", None))
        self.logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.checkBoxDebug.setText(QCoreApplication.translate("MainWindow", u"Debug", None))
        self.get_instances.setText(QCoreApplication.translate("MainWindow", u"Update instances", None))
        self.send_instance.setText(QCoreApplication.translate("MainWindow", u"Send instance", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Max time", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Solver", None))
        self.solve_instance.setText(QCoreApplication.translate("MainWindow", u"Solve instance", None))
        self.get_results.setText(QCoreApplication.translate("MainWindow", u"Get results", None))
        self.show_solution.setText(QCoreApplication.translate("MainWindow", u"Show solution", None))
        self.showLog.setText(QCoreApplication.translate("MainWindow", u"Show progress", None))
        self.exportLog.setText(QCoreApplication.translate("MainWindow", u"Export log", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Config), QCoreApplication.translate("MainWindow", u"Config", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

