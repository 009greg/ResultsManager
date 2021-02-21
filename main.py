# Shooting Results
# GHogg 2021
# V1 - 21/02/21

# This program gets results data from SUIS formatted CSV
# and saves the results into SQLite Database for long term reference and handicap calculations.

import sys
import sqlite3
from sqlite3 import Error
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget, QComboBox, QLabel


from databaseupload import importname, uploadtodatabase_50m, uploadtodatabase_3P, masterframetodb_3P, masterframetodb_50m
from importcsv import importcsvfile_3P, importcsvfile_50m
from search import Ui_ResultsSearch

# fixme If start number doesn't begin with 1, make sure names get stiched to master frame correctly

# Connect to Database


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"IOMSC_Results.db")

# Setup PyQt5 GUI


class Ui_MainWindow(QWidget):

    def __init__(self):
        super().__init__()



    def open_dialog_box(self):
        # todo Rewrite GUI in class format? Would be nice to have
        # What is the competition format?

        self.combo_box = QComboBox(self)
        self.labelcombo = QLabel(self)
        self.combo_box.setGeometry(200,120,250,30)
        comp_list = ["ISSF 50m 3P", "ISSF 50m Prone",
                     "ISSF 10m Air Rifle"]
        self.combo_box.addItems(comp_list)
        self.combo_box.currentTextChanged.connect(self.selection)
        self.labelcombo.setText("Please Select Competition Format:")
        self.labelcombo.setStyleSheet('color:blue')
        self.show()

    def selection(self):
        text = self.combo_box.currentText()

        if text == "ISSF 50m 3P":
         print("3p chosen")

         ## Format for 3P

        elif text == "ISSF 10m Air Rifle":
            print("Air Rifle Chosen")

        else:
            print("Prone chosen")
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                      "CSV Files (*.csv)", options=options)
            path = filename
            print(path)
            importcsvfile_50m(path)
            msg = QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle('Success')
            msg.setText("Upload Complete")
            msg.setInformativeText("The SIUS match data has been imported successfully")
            msg.exec_()

            anothermsg = QtWidgets.QMessageBox()
            anothermsg.setWindowTitle("Shooter Names")
            ret = anothermsg.question(self.setupUi(MainWindow), '',
                                      "Please find the start list - usually 'yourcompname_STL.csv'",
                                      anothermsg.Ok)

            if ret == anothermsg.Ok:
                filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                          "CSV Files (*.csv)", options=options)
                path = filename
                print(path)
                importname(path)

            else:
                print("No clicked - shooter name import")

            msg2 = QtWidgets.QMessageBox()
            msg2.setIcon(QtWidgets.QMessageBox.Information)
            msg2.setWindowTitle('Success')
            msg2.setText("Start Lists Uploaded")
            msg2.setInformativeText("Start List Imported Successfully")
            msg2.exec_()

            compmsg = QtWidgets.QInputDialog(self.setupUi(MainWindow))
            compmsg.setInputMode(QtWidgets.QInputDialog.TextInput)
            compmsg.setFixedSize(300, 10)
            compmsg.setOption(QtWidgets.QInputDialog.UsePlainTextEditForTextInput)
            compmsg.setWindowTitle('Competition Name')
            compmsg.setLabelText('Please Enter Competition Name (No Spaces)')

            if compmsg.exec_() == QtWidgets.QDialog.Accepted:
                uploadtodatabase_50m()
                namecomp = compmsg.textValue()
                print(namecomp)
                masterframetodb_50m(namecomp)
                msg3 = QtWidgets.QMessageBox()
                msg3.setIcon(QtWidgets.QMessageBox.Information)
                msg3.setWindowTitle('Success')
                msg3.setInformativeText("Database upload complete")
                msg3.exec_()
            else:
                print('Cancel')

    def searchwindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ResultsSearch()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ImportCSV = QtWidgets.QPushButton(self.centralwidget)
        self.ImportCSV.setGeometry(QtCore.QRect(20, 480, 231, 33))
        self.ImportCSV.setObjectName("ImportCSV")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(210, 40, 351, 150))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("index.png"))
        self.label_3.setObjectName("label_3")
        self.searchbtn = QtWidgets.QPushButton(self.centralwidget)
        self.searchbtn.setGeometry(QtCore.QRect(600, 480, 141, 33))
        self.searchbtn.setObjectName("ResultsSearch")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 400, 81, 71))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("excel.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(620, 390, 91, 81))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("search.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionThis = QtWidgets.QAction(MainWindow)
        self.actionThis.setObjectName("actionThis")
        self.actionsomething = QtWidgets.QAction(MainWindow)
        self.actionsomething.setObjectName("actionsomething")
        self.actionAdd_New_Member = QtWidgets.QAction(MainWindow)
        self.actionAdd_New_Member.setObjectName("actionAdd_New_Member")
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Button functions
        self.searchbtn.clicked.connect(self.searchwindow)
        self.ImportCSV.clicked.connect(self.open_dialog_box)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("IOM Shooting Club Results Manager", "IOM Shooting Club Results Manager"))
        self.ImportCSV.setText(_translate("MainWindow", "Import CSV to Results Database"))
        self.searchbtn.setText(_translate("MainWindow", "Stats"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionThis.setText(_translate("MainWindow", "This"))
        self.actionsomething.setText(_translate("MainWindow", "something"))
        self.actionAdd_New_Member.setText(_translate("MainWindow", "Add New Member"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
