# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fu.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 121, 201))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox_uart_num = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_uart_num.setObjectName("comboBox_uart_num")
        self.verticalLayout.addWidget(self.comboBox_uart_num)
        self.comboBox_rate = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_rate.setObjectName("comboBox_rate")
        self.comboBox_rate.addItem("")
        self.comboBox_rate.addItem("")
        self.comboBox_rate.addItem("")
        self.comboBox_rate.addItem("")
        self.comboBox_rate.addItem("")
        self.comboBox_rate.addItem("")
        self.verticalLayout.addWidget(self.comboBox_rate)
        self.button_start_uart = QtWidgets.QPushButton(self.groupBox)
        self.button_start_uart.setObjectName("button_start_uart")
        self.verticalLayout.addWidget(self.button_start_uart)
        self.button_close_uart = QtWidgets.QPushButton(self.groupBox)
        self.button_close_uart.setObjectName("button_close_uart")
        self.verticalLayout.addWidget(self.button_close_uart)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(120, 0, 681, 201))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit_send_data = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_send_data.setGeometry(QtCore.QRect(0, 220, 211, 251))
        self.textEdit_send_data.setObjectName("textEdit_send_data")
        self.button_send_data = QtWidgets.QPushButton(self.centralwidget)
        self.button_send_data.setGeometry(QtCore.QRect(50, 480, 93, 28))
        self.button_send_data.setObjectName("button_send_data")
        self.button_clear = QtWidgets.QPushButton(self.centralwidget)
        self.button_clear.setGeometry(QtCore.QRect(50, 510, 93, 28))
        self.button_clear.setObjectName("button_clear")
        self.label_view = QtWidgets.QLabel(self.centralwidget)
        self.label_view.setGeometry(QtCore.QRect(230, 220, 561, 251))
        self.label_view.setObjectName("label_view")
        self.button_end = QtWidgets.QPushButton(self.centralwidget)
        self.button_end.setGeometry(QtCore.QRect(710, 510, 93, 28))
        self.button_end.setObjectName("button_end")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "串口设置"))
        self.comboBox_rate.setItemText(0, _translate("MainWindow", "9600"))
        self.comboBox_rate.setItemText(1, _translate("MainWindow", "38400"))
        self.comboBox_rate.setItemText(2, _translate("MainWindow", "115200"))
        self.comboBox_rate.setItemText(3, _translate("MainWindow", "230400"))
        self.comboBox_rate.setItemText(4, _translate("MainWindow", "921600"))
        self.comboBox_rate.setItemText(5, _translate("MainWindow", "1382400"))
        self.button_start_uart.setText(_translate("MainWindow", "打开串口"))
        self.button_close_uart.setText(_translate("MainWindow", "关闭串口"))
        self.button_send_data.setText(_translate("MainWindow", "发送"))
        self.button_clear.setText(_translate("MainWindow", "清除"))
        self.label_view.setText(_translate("MainWindow", "图像显示"))
        self.button_end.setText(_translate("MainWindow", "退出程序"))

