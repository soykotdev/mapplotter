from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 250)

        style_file = QtCore.QFile(":/styles.qss")
        style_file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        stream = QtCore.QTextStream(style_file)
        QtWidgets.QApplication.instance().setStyleSheet(stream.readAll())
        style_file.close()

        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(30, 20, 341, 170))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setObjectName("label")
        self.label.setText("Layer Name")

        self.comboBoxLayer = QtWidgets.QComboBox(self.splitter)
        self.comboBoxLayer.setObjectName("comboBoxLayer")

        self.labelField = QtWidgets.QLabel(self.splitter)
        self.labelField.setObjectName("labelField")
        self.labelField.setText("Field Name")

        self.comboBoxField = QtWidgets.QComboBox(self.splitter)
        self.comboBoxField.setObjectName("comboBoxField")

        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setObjectName("label_2")
        self.label_2.setText("Starting plot number")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.splitter)
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 200, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # Copyright symbol and text at the bottom of the dialog
        self.labelCopyright = QtWidgets.QLabel(Dialog)
        self.labelCopyright.setGeometry(QtCore.QRect(30, 230, 341, 16))
        self.labelCopyright.setObjectName("labelCopyright")
        self.labelCopyright.setAlignment(QtCore.Qt.AlignCenter)
        self.labelCopyright.setText("© GIS Division, SMEC,BD")
        self.labelCopyright.setFont(QtGui.QFont("Arial", 5))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MapPlotter"))
