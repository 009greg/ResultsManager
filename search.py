from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from sqlite3 import Error

# Connect to Database


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def get_data_from_db(conn, name):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    #cur.execute("SELECT {} FROM Shooters".format(name))
    cur.execute("SELECT 'FirstName' FROM Shooters")
    rows = cur.fetchall()


    for row in rows:
        if row == name:
          print(row)


database = r"IOMSC_Results.db"
conn = create_connection(database)


#Todo Run a database search for name and display x (handicaps,average,etc)
class Ui_ResultsSearch(object):
    def setupUi(self, ResultsSearch):
        ResultsSearch.setObjectName("ResultsSearch")
        ResultsSearch.resize(573, 395)
        self.label = QtWidgets.QLabel(ResultsSearch)
        self.label.setGeometry(QtCore.QRect(130, 20, 400, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ResultsSearch)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 131, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.ShooterDetailsIn = QtWidgets.QLineEdit(ResultsSearch)
        self.ShooterDetailsIn.setGeometry(QtCore.QRect(160, 90, 191, 31))
        self.ShooterDetailsIn.setObjectName("ShooterDetailsIn")
        self.ShooterDetailsOut = QtWidgets.QListWidget(ResultsSearch)
        self.ShooterDetailsOut.setGeometry(QtCore.QRect(160, 170, 256, 192))
        self.ShooterDetailsOut.setObjectName("ShooterDetailsOut")


        # GUI Functions
        #todo Get text from shooter details in and display in list object in GUI

        self.retranslateUi(ResultsSearch)
        QtCore.QMetaObject.connectSlotsByName(ResultsSearch)


    def retranslateUi(self, ResultsSearch):
        _translate = QtCore.QCoreApplication.translate
        ResultsSearch.setWindowTitle(_translate("ResultsSearch", "Frame"))
        self.label.setText(_translate("ResultsSearch", "Shooter Stats"))
        self.label_2.setText(_translate("ResultsSearch", "Name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ResultsSearch = QtWidgets.QFrame()
    ui = Ui_ResultsSearch()
    ui.setupUi(ResultsSearch)
    ResultsSearch.show()
    sys.exit(app.exec_())
