# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/turboss/Proyectos/JauriaCNC/build/lib.linux-x86_64-2.7/jcnc/ui/window.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1119, 807)
        Form.setFocusPolicy(QtCore.Qt.StrongFocus)
        Form.setToolTipDuration(-1)
        Form.setProperty("promptAtExit", False)
        Form.setProperty("promot_on_exit", False)
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.estop_abutton = ActionButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.estop_abutton.sizePolicy().hasHeightForWidth())
        self.estop_abutton.setSizePolicy(sizePolicy)
        self.estop_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.estop_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.estop_abutton.setCheckable(True)
        self.estop_abutton.setObjectName("estop_abutton")
        self.horizontalLayout_6.addWidget(self.estop_abutton)
        self.power_abutton = ActionButton(self.centralwidget)
        self.power_abutton.setEnabled(False)
        self.power_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.power_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.power_abutton.setCheckable(False)
        self.power_abutton.setObjectName("power_abutton")
        self.horizontalLayout_6.addWidget(self.power_abutton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.actionbutton_27 = ActionButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_27.sizePolicy().hasHeightForWidth())
        self.actionbutton_27.setSizePolicy(sizePolicy)
        self.actionbutton_27.setMinimumSize(QtCore.QSize(50, 50))
        self.actionbutton_27.setMaximumSize(QtCore.QSize(50, 50))
        self.actionbutton_27.setCheckable(True)
        self.actionbutton_27.setAutoExclusive(True)
        self.actionbutton_27.setObjectName("actionbutton_27")
        self.horizontalLayout_8.addWidget(self.actionbutton_27)
        self.actionbutton_28 = ActionButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_28.sizePolicy().hasHeightForWidth())
        self.actionbutton_28.setSizePolicy(sizePolicy)
        self.actionbutton_28.setMinimumSize(QtCore.QSize(50, 50))
        self.actionbutton_28.setMaximumSize(QtCore.QSize(50, 50))
        self.actionbutton_28.setCheckable(True)
        self.actionbutton_28.setAutoExclusive(True)
        self.actionbutton_28.setObjectName("actionbutton_28")
        self.horizontalLayout_8.addWidget(self.actionbutton_28)
        self.actionbutton_29 = ActionButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_29.sizePolicy().hasHeightForWidth())
        self.actionbutton_29.setSizePolicy(sizePolicy)
        self.actionbutton_29.setMinimumSize(QtCore.QSize(50, 50))
        self.actionbutton_29.setMaximumSize(QtCore.QSize(50, 50))
        self.actionbutton_29.setCheckable(True)
        self.actionbutton_29.setAutoExclusive(True)
        self.actionbutton_29.setObjectName("actionbutton_29")
        self.horizontalLayout_8.addWidget(self.actionbutton_29)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_8)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.home_label = QtWidgets.QLabel(self.centralwidget)
        self.home_label.setObjectName("home_label")
        self.horizontalLayout_2.addWidget(self.home_label)
        self.homeall_abutton = ActionButton(self.centralwidget)
        self.homeall_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.homeall_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.homeall_abutton.setObjectName("homeall_abutton")
        self.horizontalLayout_2.addWidget(self.homeall_abutton)
        spacerItem3 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.homex_abutton = ActionButton(self.centralwidget)
        self.homex_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.homex_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.homex_abutton.setObjectName("homex_abutton")
        self.horizontalLayout_3.addWidget(self.homex_abutton)
        self.homey_abutton = ActionButton(self.centralwidget)
        self.homey_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.homey_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.homey_abutton.setObjectName("homey_abutton")
        self.horizontalLayout_3.addWidget(self.homey_abutton)
        self.homez_abutton = ActionButton(self.centralwidget)
        self.homez_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.homez_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.homez_abutton.setObjectName("homez_abutton")
        self.horizontalLayout_3.addWidget(self.homez_abutton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.zero_dbutton = DialogButton(self.centralwidget)
        self.zero_dbutton.setMinimumSize(QtCore.QSize(50, 50))
        self.zero_dbutton.setMaximumSize(QtCore.QSize(50, 50))
        self.zero_dbutton.setObjectName("zero_dbutton")
        self.horizontalLayout_2.addWidget(self.zero_dbutton)
        spacerItem5 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.run_abutton = ActionButton(self.centralwidget)
        self.run_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.run_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.run_abutton.setObjectName("run_abutton")
        self.horizontalLayout_7.addWidget(self.run_abutton)
        self.pause_abutton = ActionButton(self.centralwidget)
        self.pause_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.pause_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.pause_abutton.setObjectName("pause_abutton")
        self.horizontalLayout_7.addWidget(self.pause_abutton)
        self.stop_abutton = ActionButton(self.centralwidget)
        self.stop_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.stop_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.stop_abutton.setObjectName("stop_abutton")
        self.horizontalLayout_7.addWidget(self.stop_abutton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout_7)
        spacerItem6 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(5, 0, 3, 15)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gcodebackplot = GcodeBackplot(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gcodebackplot.sizePolicy().hasHeightForWidth())
        self.gcodebackplot.setSizePolicy(sizePolicy)
        self.gcodebackplot.setStyleSheet("")
        self.gcodebackplot.setObjectName("gcodebackplot")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.gcodebackplot)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 191, 91))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.DRO = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.DRO.setContentsMargins(0, 0, 0, 0)
        self.DRO.setObjectName("DRO")
        self.x_dro = StatusLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.x_dro.setFont(font)
        self.x_dro.setObjectName("x_dro")
        self.DRO.addWidget(self.x_dro)
        self.y_dro = StatusLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.y_dro.setFont(font)
        self.y_dro.setObjectName("y_dro")
        self.DRO.addWidget(self.y_dro)
        self.z_dro = StatusLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.z_dro.setFont(font)
        self.z_dro.setObjectName("z_dro")
        self.DRO.addWidget(self.z_dro)
        self.comboBox = QtWidgets.QComboBox(self.gcodebackplot)
        self.comboBox.setGeometry(QtCore.QRect(200, 10, 79, 23))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayoutWidget.raise_()
        self.comboBox.raise_()
        self.verticalLayout_4.addWidget(self.gcodebackplot)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.jogyplus_abutton = ActionButton(self.centralwidget)
        self.jogyplus_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.jogyplus_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.jogyplus_abutton.setObjectName("jogyplus_abutton")
        self.gridLayout.addWidget(self.jogyplus_abutton, 0, 2, 1, 1)
        self.jogxmin_abutton = ActionButton(self.centralwidget)
        self.jogxmin_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.jogxmin_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.jogxmin_abutton.setObjectName("jogxmin_abutton")
        self.gridLayout.addWidget(self.jogxmin_abutton, 1, 1, 1, 1)
        self.jogxplus_abutton = ActionButton(self.centralwidget)
        self.jogxplus_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.jogxplus_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.jogxplus_abutton.setObjectName("jogxplus_abutton")
        self.gridLayout.addWidget(self.jogxplus_abutton, 1, 3, 1, 1)
        self.jogymin_abutton = ActionButton(self.centralwidget)
        self.jogymin_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.jogymin_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.jogymin_abutton.setObjectName("jogymin_abutton")
        self.gridLayout.addWidget(self.jogymin_abutton, 1, 2, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.jogzmin_abutton = ActionButton(self.centralwidget)
        self.jogzmin_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.jogzmin_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.jogzmin_abutton.setObjectName("jogzmin_abutton")
        self.gridLayout_2.addWidget(self.jogzmin_abutton, 1, 0, 1, 1)
        self.jogzplus_abutton = ActionButton(self.centralwidget)
        self.jogzplus_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.jogzplus_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.jogzplus_abutton.setObjectName("jogzplus_abutton")
        self.gridLayout_2.addWidget(self.jogzplus_abutton, 0, 0, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_2)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem9)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.feedover_slabel = StatusLabel(self.centralwidget)
        self.feedover_slabel.setAlignment(QtCore.Qt.AlignCenter)
        self.feedover_slabel.setObjectName("feedover_slabel")
        self.verticalLayout_3.addWidget(self.feedover_slabel)
        self.feedover_aslider = ActionSlider(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.feedover_aslider.sizePolicy().hasHeightForWidth())
        self.feedover_aslider.setSizePolicy(sizePolicy)
        self.feedover_aslider.setMinimumSize(QtCore.QSize(300, 50))
        self.feedover_aslider.setMaximumSize(QtCore.QSize(300, 50))
        self.feedover_aslider.setOrientation(QtCore.Qt.Horizontal)
        self.feedover_aslider.setObjectName("feedover_aslider")
        self.verticalLayout_3.addWidget(self.feedover_aslider)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem10)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setSpacing(10)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.spindleon_abutton = ActionButton(self.centralwidget)
        self.spindleon_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.spindleon_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.spindleon_abutton.setObjectName("spindleon_abutton")
        self.gridLayout_3.addWidget(self.spindleon_abutton, 0, 0, 1, 1)
        self.spindleoff_abutton = ActionButton(self.centralwidget)
        self.spindleoff_abutton.setMinimumSize(QtCore.QSize(50, 50))
        self.spindleoff_abutton.setMaximumSize(QtCore.QSize(50, 50))
        self.spindleoff_abutton.setObjectName("spindleoff_abutton")
        self.gridLayout_3.addWidget(self.spindleoff_abutton, 1, 0, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_3)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem11)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.gcodeeditor = GcodeEditor(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gcodeeditor.sizePolicy().hasHeightForWidth())
        self.gcodeeditor.setSizePolicy(sizePolicy)
        self.gcodeeditor.setMinimumSize(QtCore.QSize(330, 0))
        self.gcodeeditor.setMaximumSize(QtCore.QSize(610, 16777215))
        self.gcodeeditor.setObjectName("gcodeeditor")
        self.verticalLayout_5.addWidget(self.gcodeeditor)
        self.mdi_entry_box = MDIEntry(self.centralwidget)
        self.mdi_entry_box.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(14)
        self.mdi_entry_box.setFont(font)
        self.mdi_entry_box.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mdi_entry_box.setObjectName("mdi_entry_box")
        self.verticalLayout_5.addWidget(self.mdi_entry_box)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_5.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        Form.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(Form)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1119, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuExit = QtWidgets.QMenu(self.menuBar)
        self.menuExit.setObjectName("menuExit")
        self.menuRecentFiles = QtWidgets.QMenu(self.menuExit)
        self.menuRecentFiles.setObjectName("menuRecentFiles")
        self.menuMachine = QtWidgets.QMenu(self.menuBar)
        self.menuMachine.setObjectName("menuMachine")
        self.menuHoming = QtWidgets.QMenu(self.menuMachine)
        self.menuHoming.setObjectName("menuHoming")
        self.menuCooling = QtWidgets.QMenu(self.menuMachine)
        self.menuCooling.setObjectName("menuCooling")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        Form.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(Form)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen = QtWidgets.QAction(Form)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(Form)
        self.actionClose.setObjectName("actionClose")
        self.actionReload = QtWidgets.QAction(Form)
        self.actionReload.setObjectName("actionReload")
        self.actionSave_As = QtWidgets.QAction(Form)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionHome_X = QtWidgets.QAction(Form)
        self.actionHome_X.setObjectName("actionHome_X")
        self.actionHome_Y = QtWidgets.QAction(Form)
        self.actionHome_Y.setObjectName("actionHome_Y")
        self.actionHome_Z = QtWidgets.QAction(Form)
        self.actionHome_Z.setObjectName("actionHome_Z")
        self.action_EmergencyStop_toggle = QtWidgets.QAction(Form)
        self.action_EmergencyStop_toggle.setObjectName("action_EmergencyStop_toggle")
        self.action_MachinePower_toggle = QtWidgets.QAction(Form)
        self.action_MachinePower_toggle.setObjectName("action_MachinePower_toggle")
        self.actionHome_All = QtWidgets.QAction(Form)
        self.actionHome_All.setObjectName("actionHome_All")
        self.actionRun_Program = QtWidgets.QAction(Form)
        self.actionRun_Program.setObjectName("actionRun_Program")
        self.actionFile1 = QtWidgets.QAction(Form)
        self.actionFile1.setObjectName("actionFile1")
        self.actionReport_Actual_Position = QtWidgets.QAction(Form)
        self.actionReport_Actual_Position.setCheckable(True)
        self.actionReport_Actual_Position.setObjectName("actionReport_Actual_Position")
        self.actionTest = QtWidgets.QAction(Form)
        self.actionTest.setObjectName("actionTest")
        self.action_Mist_toggle = QtWidgets.QAction(Form)
        self.action_Mist_toggle.setCheckable(True)
        self.action_Mist_toggle.setObjectName("action_Mist_toggle")
        self.action_Flood_toggle = QtWidgets.QAction(Form)
        self.action_Flood_toggle.setCheckable(True)
        self.action_Flood_toggle.setObjectName("action_Flood_toggle")
        self.action_program_run = QtWidgets.QAction(Form)
        self.action_program_run.setObjectName("action_program_run")
        self.action_coolant_floodToggle = QtWidgets.QAction(Form)
        self.action_coolant_floodToggle.setCheckable(True)
        self.action_coolant_floodToggle.setObjectName("action_coolant_floodToggle")
        self.actionHalshow = QtWidgets.QAction(Form)
        self.actionHalshow.setObjectName("actionHalshow")
        self.actionHalmeter = QtWidgets.QAction(Form)
        self.actionHalmeter.setObjectName("actionHalmeter")
        self.actionHAL_Scope = QtWidgets.QAction(Form)
        self.actionHAL_Scope.setObjectName("actionHAL_Scope")
        self.actionCalibration = QtWidgets.QAction(Form)
        self.actionCalibration.setObjectName("actionCalibration")
        self.actionOverride_Limits = QtWidgets.QAction(Form)
        self.actionOverride_Limits.setObjectName("actionOverride_Limits")
        self.actionOverride_Limits_2 = QtWidgets.QAction(Form)
        self.actionOverride_Limits_2.setObjectName("actionOverride_Limits_2")
        self.actionRun_From_Line = QtWidgets.QAction(Form)
        self.actionRun_From_Line.setObjectName("actionRun_From_Line")
        self.actionStep = QtWidgets.QAction(Form)
        self.actionStep.setObjectName("actionStep")
        self.actionPause = QtWidgets.QAction(Form)
        self.actionPause.setObjectName("actionPause")
        self.actionStop = QtWidgets.QAction(Form)
        self.actionStop.setObjectName("actionStop")
        self.actionResume = QtWidgets.QAction(Form)
        self.actionResume.setObjectName("actionResume")
        self.actionPause_at_M1 = QtWidgets.QAction(Form)
        self.actionPause_at_M1.setObjectName("actionPause_at_M1")
        self.actionSkip_lines_with = QtWidgets.QAction(Form)
        self.actionSkip_lines_with.setObjectName("actionSkip_lines_with")
        self.menuRecentFiles.addAction(self.actionFile1)
        self.menuExit.addAction(self.actionOpen)
        self.menuExit.addAction(self.menuRecentFiles.menuAction())
        self.menuExit.addAction(self.actionReload)
        self.menuExit.addAction(self.actionClose)
        self.menuExit.addAction(self.actionSave_As)
        self.menuExit.addSeparator()
        self.menuExit.addAction(self.actionExit)
        self.menuHoming.addAction(self.actionHome_All)
        self.menuHoming.addAction(self.actionHome_X)
        self.menuHoming.addAction(self.actionHome_Y)
        self.menuHoming.addAction(self.actionHome_Z)
        self.menuCooling.addAction(self.action_Mist_toggle)
        self.menuCooling.addAction(self.action_Flood_toggle)
        self.menuMachine.addAction(self.action_EmergencyStop_toggle)
        self.menuMachine.addAction(self.action_MachinePower_toggle)
        self.menuMachine.addSeparator()
        self.menuMachine.addAction(self.actionRun_Program)
        self.menuMachine.addAction(self.actionRun_From_Line)
        self.menuMachine.addAction(self.actionStep)
        self.menuMachine.addAction(self.actionPause)
        self.menuMachine.addAction(self.actionResume)
        self.menuMachine.addAction(self.actionStop)
        self.menuMachine.addAction(self.actionPause_at_M1)
        self.menuMachine.addAction(self.actionSkip_lines_with)
        self.menuMachine.addSeparator()
        self.menuMachine.addAction(self.menuHoming.menuAction())
        self.menuMachine.addAction(self.menuCooling.menuAction())
        self.menuMachine.addSeparator()
        self.menuMachine.addAction(self.actionOverride_Limits)
        self.menuTools.addAction(self.actionHalmeter)
        self.menuTools.addAction(self.actionHalshow)
        self.menuTools.addAction(self.actionHAL_Scope)
        self.menuTools.addAction(self.actionCalibration)
        self.menuBar.addAction(self.menuExit.menuAction())
        self.menuBar.addAction(self.menuMachine.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())

        self.retranslateUi(Form)
        self.comboBox.currentTextChanged['QString'].connect(self.gcodebackplot.setView)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "JAURIA CNC"))
        self.estop_abutton.setText(_translate("Form", "E-STOP"))
        self.estop_abutton.setProperty("actionName", _translate("Form", "machine.estop.toggle"))
        self.power_abutton.setText(_translate("Form", "POWER"))
        self.power_abutton.setProperty("actionName", _translate("Form", "machine.power.toggle"))
        self.label.setText(_translate("Form", "MODE"))
        self.actionbutton_27.setText(_translate("Form", "MAN"))
        self.actionbutton_27.setProperty("actionName", _translate("Form", "machine.mode.manual"))
        self.actionbutton_27.setProperty("position", _translate("Form", "first"))
        self.actionbutton_27.setProperty("styleClass", _translate("Form", "option"))
        self.actionbutton_28.setText(_translate("Form", "AUTO"))
        self.actionbutton_28.setProperty("actionName", _translate("Form", "machine.mode.auto"))
        self.actionbutton_28.setProperty("styleClass", _translate("Form", "option"))
        self.actionbutton_29.setText(_translate("Form", "MDI"))
        self.actionbutton_29.setProperty("actionName", _translate("Form", "machine.mode.mdi"))
        self.actionbutton_29.setProperty("position", _translate("Form", "last"))
        self.actionbutton_29.setProperty("styleClass", _translate("Form", "option"))
        self.home_label.setText(_translate("Form", "HOME"))
        self.homeall_abutton.setText(_translate("Form", "ALL"))
        self.homeall_abutton.setProperty("actionName", _translate("Form", "machine.home.all"))
        self.homex_abutton.setText(_translate("Form", "X"))
        self.homex_abutton.setProperty("actionName", _translate("Form", "machine.home.axis:x"))
        self.homey_abutton.setText(_translate("Form", "Y"))
        self.homey_abutton.setProperty("actionName", _translate("Form", "machine.home.axis:y"))
        self.homez_abutton.setText(_translate("Form", "Z"))
        self.homez_abutton.setProperty("actionName", _translate("Form", "machine.home.axis:z"))
        self.label_2.setText(_translate("Form", "PART"))
        self.zero_dbutton.setText(_translate("Form", "ZERO"))
        self.zero_dbutton.setProperty("dialogName", _translate("Form", "set_work_offsets"))
        self.label_3.setText(_translate("Form", "PROGRAM"))
        self.run_abutton.setText(_translate("Form", "RUN"))
        self.run_abutton.setProperty("actionName", _translate("Form", "program.run"))
        self.pause_abutton.setText(_translate("Form", "PAUSE"))
        self.pause_abutton.setProperty("actionName", _translate("Form", "program.pause"))
        self.stop_abutton.setText(_translate("Form", "STOP"))
        self.stop_abutton.setProperty("actionName", _translate("Form", "program.abort"))
        self.x_dro.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:axis?rel\", \"trigger\": true}, {\"url\": \"status:program_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"X {: 7.4f}\\\".format(ch[0][0]) if ch[1] == \'in\' else \\\"X {: 7.3f}\\\".format(ch[0][0])\", \"name\": \"rel pos\"}]"))
        self.y_dro.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:axis?rel\", \"trigger\": true}, {\"url\": \"status:program_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"Y {: 7.4f}\\\".format(ch[0][1]) if ch[1] == \'in\' else \\\"Y {: 7.3f}\\\".format(ch[0][1])\", \"name\": \"rel pos\"}]"))
        self.z_dro.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:axis?rel\", \"trigger\": true}, {\"url\": \"status:program_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"Z {: 7.4f}\\\".format(ch[0][2]) if ch[1] == \'in\' else \\\"Z {: 7.3f}\\\".format(ch[0][2])\", \"name\": \"rel pos\"}]"))
        self.comboBox.setItemText(0, _translate("Form", "p"))
        self.comboBox.setItemText(1, _translate("Form", "x"))
        self.comboBox.setItemText(2, _translate("Form", "y"))
        self.comboBox.setItemText(3, _translate("Form", "z"))
        self.comboBox.setItemText(4, _translate("Form", "z2"))
        self.jogyplus_abutton.setText(_translate("Form", "+Y"))
        self.jogyplus_abutton.setProperty("actionName", _translate("Form", "machine.jog.axis:y,pos"))
        self.jogxmin_abutton.setText(_translate("Form", "-X"))
        self.jogxmin_abutton.setProperty("actionName", _translate("Form", "machine.jog.axis:x,neg"))
        self.jogxplus_abutton.setText(_translate("Form", "+X"))
        self.jogxplus_abutton.setProperty("actionName", _translate("Form", "machine.jog.axis:x,pos"))
        self.jogymin_abutton.setText(_translate("Form", "-Y"))
        self.jogymin_abutton.setProperty("actionName", _translate("Form", "machine.jog.axis:y,neg"))
        self.jogzmin_abutton.setText(_translate("Form", "-Z"))
        self.jogzmin_abutton.setProperty("actionName", _translate("Form", "machine.jog.axis:z,neg"))
        self.jogzplus_abutton.setText(_translate("Form", "+Z"))
        self.jogzplus_abutton.setProperty("actionName", _translate("Form", "machine.jog.axis:z,pos"))
        self.feedover_slabel.setText(_translate("Form", "Feed Override: 0%"))
        self.feedover_slabel.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:feedrate\",\n"
"                \"trigger\": true, \n"
"                \"type\": \"float\"\n"
"            }\n"
"        ], \n"
"        \"expression\": \"\\\"Feed Override: {:.0%}\\\".format(ch[0])\", \n"
"        \"name\": \"New Rule\", \n"
"        \"property\": \"Text\"\n"
"    }\n"
"]"))
        self.feedover_slabel.setProperty("format", _translate("Form", "<b>Feed Override:</b> {:.0%}"))
        self.feedover_slabel.setProperty("statusItem", _translate("Form", "feedrate"))
        self.feedover_aslider.setProperty("actionName", _translate("Form", "machine.feed-override.set"))
        self.label_4.setText(_translate("Form", "SPINDLE"))
        self.spindleon_abutton.setText(_translate("Form", "ON"))
        self.spindleon_abutton.setProperty("actionName", _translate("Form", "spindle.forward"))
        self.spindleoff_abutton.setText(_translate("Form", "OFF"))
        self.spindleoff_abutton.setProperty("actionName", _translate("Form", "spindle.off"))
        self.gcodeeditor.setProperty("backgroundcolor", _translate("Form", "#454545"))
        self.gcodeeditor.setProperty("marginbackgroundcolor", _translate("Form", "#5c5c5c"))
        self.gcodeeditor.setProperty("thingstyle", _translate("Form", "#ffffff"))
        self.mdi_entry_box.setPlaceholderText(_translate("Form", "MDI"))
        self.pushButton.setText(_translate("Form", "PushButton"))
        self.menuExit.setTitle(_translate("Form", "File"))
        self.menuRecentFiles.setTitle(_translate("Form", "Recent &Files"))
        self.menuMachine.setTitle(_translate("Form", "Machine"))
        self.menuHoming.setTitle(_translate("Form", "Homing"))
        self.menuCooling.setTitle(_translate("Form", "Cooling"))
        self.menuTools.setTitle(_translate("Form", "Tools"))
        self.actionExit.setText(_translate("Form", "Exit"))
        self.actionOpen.setText(_translate("Form", "&Open ..."))
        self.actionOpen.setShortcut(_translate("Form", "O"))
        self.actionClose.setText(_translate("Form", "Close"))
        self.actionReload.setText(_translate("Form", "&Reload"))
        self.actionReload.setShortcut(_translate("Form", "Ctrl+R"))
        self.actionSave_As.setText(_translate("Form", "Save As ..."))
        self.actionHome_X.setText(_translate("Form", "Home &X"))
        self.actionHome_Y.setText(_translate("Form", "Home &Y"))
        self.actionHome_Z.setText(_translate("Form", "Home &Z"))
        self.action_EmergencyStop_toggle.setText(_translate("Form", "Toggle E-stop"))
        self.action_EmergencyStop_toggle.setShortcut(_translate("Form", "F1"))
        self.action_EmergencyStop_toggle.setProperty("actionName", _translate("Form", "machine.estop.toggle"))
        self.action_MachinePower_toggle.setText(_translate("Form", "Machine Power"))
        self.action_MachinePower_toggle.setShortcut(_translate("Form", "F2"))
        self.action_MachinePower_toggle.setProperty("actionName", _translate("Form", "machine.power.toggle"))
        self.actionHome_All.setText(_translate("Form", "Home All"))
        self.actionHome_All.setShortcut(_translate("Form", "Home"))
        self.actionRun_Program.setText(_translate("Form", "Run Program"))
        self.actionRun_Program.setShortcut(_translate("Form", "R"))
        self.actionRun_Program.setProperty("actionName", _translate("Form", "program.run"))
        self.actionFile1.setText(_translate("Form", "File1"))
        self.actionReport_Actual_Position.setText(_translate("Form", "Report Actual Position"))
        self.actionTest.setText(_translate("Form", "Test"))
        self.action_Mist_toggle.setText(_translate("Form", "Mist"))
        self.action_Mist_toggle.setShortcut(_translate("Form", "F7"))
        self.action_Mist_toggle.setProperty("actionName", _translate("Form", "coolant.mist.toggle"))
        self.action_Flood_toggle.setText(_translate("Form", "Flood"))
        self.action_Flood_toggle.setShortcut(_translate("Form", "F8"))
        self.action_Flood_toggle.setProperty("actionName", _translate("Form", "coolant.flood.toggle"))
        self.action_program_run.setText(_translate("Form", "Run Program"))
        self.action_coolant_floodToggle.setText(_translate("Form", "Flood"))
        self.actionHalshow.setText(_translate("Form", "HAL Show"))
        self.actionHalshow.setProperty("actionName", _translate("Form", "tool.halshow"))
        self.actionHalmeter.setText(_translate("Form", "HAL Meter"))
        self.actionHalmeter.setProperty("actionName", _translate("Form", "tool.halmeter"))
        self.actionHAL_Scope.setText(_translate("Form", "HAL Scope"))
        self.actionHAL_Scope.setProperty("actionName", _translate("Form", "tool.halscope"))
        self.actionCalibration.setText(_translate("Form", "Calibration"))
        self.actionCalibration.setProperty("actionName", _translate("Form", "tool.calibration"))
        self.actionOverride_Limits.setText(_translate("Form", "Override Limits"))
        self.actionOverride_Limits.setProperty("actionName", _translate("Form", "machine.override-limits"))
        self.actionOverride_Limits_2.setText(_translate("Form", "Override Limits"))
        self.actionOverride_Limits_2.setProperty("actionName", _translate("Form", "machine.override-limits"))
        self.actionRun_From_Line.setText(_translate("Form", "Run From Line"))
        self.actionRun_From_Line.setProperty("actionName", _translate("Form", "program.run-from-line"))
        self.actionStep.setText(_translate("Form", "Step"))
        self.actionStep.setShortcut(_translate("Form", "T"))
        self.actionStep.setProperty("actionName", _translate("Form", "program.step"))
        self.actionPause.setText(_translate("Form", "Pause"))
        self.actionPause.setShortcut(_translate("Form", "P"))
        self.actionPause.setProperty("actionName", _translate("Form", "program.pause"))
        self.actionStop.setText(_translate("Form", "Stop"))
        self.actionStop.setShortcut(_translate("Form", "Esc"))
        self.actionStop.setProperty("actionName", _translate("Form", "program.abort"))
        self.actionResume.setText(_translate("Form", "Resume"))
        self.actionResume.setShortcut(_translate("Form", "S"))
        self.actionResume.setProperty("actionName", _translate("Form", "program.resume"))
        self.actionPause_at_M1.setText(_translate("Form", "Pause at \'M1\'"))
        self.actionPause_at_M1.setProperty("actionName", _translate("Form", "program.optional-stop.toggle"))
        self.actionSkip_lines_with.setText(_translate("Form", "Skip lines with \'/\'"))
        self.actionSkip_lines_with.setProperty("actionName", _translate("Form", "program.block-delete.toggle"))

from qtpyvcp.widgets.button_widgets.action_button import ActionButton
from qtpyvcp.widgets.button_widgets.dialog_button import DialogButton
from qtpyvcp.widgets.display_widgets.gcode_backplot import GcodeBackplot
from qtpyvcp.widgets.display_widgets.status_label import StatusLabel
from qtpyvcp.widgets.form_widgets.main_window import VCPMainWindow
from qtpyvcp.widgets.input_widgets.action_slider import ActionSlider
from qtpyvcp.widgets.input_widgets.gcode_editor import GcodeEditor
from qtpyvcp.widgets.input_widgets.mdientry_widget import MDIEntry
import resources_rc
