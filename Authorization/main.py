import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QFileDialog, QLabel, QGridLayout, QLineEdit, QComboBox, QAbstractItemView, \
    QCalendarWidget, QMessageBox
from PyQt5.QtGui import QColor
from StaticResources import TableData
class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация нового пользователя")
        self.UI()
    def UI(self):
        flag = 0
        self.StaticElementsCount = 8
        self.layout = QGridLayout()
        self.SurnameTextBox = QLineEdit()
        self.Name = QLineEdit()
        self.FatherName = QLineEdit()
        self.Post = QLineEdit()
        self.Contacts = QLineEdit()
        self.Login = QLineEdit()
        self.Password = QLineEdit()
        self.ComboBox = QComboBox()
        self.ComboBox.addItems(["ВК", "ОВУ", "ВВУЗ", "ГУК"])
        #self.ComboBox.currentIndexChanged.connect(self.changedComboBox())
        self.ComboBox.currentTextChanged.connect(self.changedComboBox)
        self.lineEdits = [self.SurnameTextBox, self.Name, self.FatherName, self.Post,self.Contacts,  self.Login, self.Password, self.ComboBox]
        lineEditNames = ["Фамилия", "Имя", "Отчество", "Должность", "Контакты", "Логин", "Пароль", "Тип организации"]
        self.setLayout(self.layout)
        for i in range(self.StaticElementsCount):
            self.layout.addWidget(QLabel(lineEditNames[i]), i + flag, 0)
            self.layout.addWidget(self.lineEdits[i], i + flag, 1)
            self.layout.setRowMinimumHeight(i + flag, 10)
        self.createVK_UI()
    def addButtons(self, row:int):

        self.CancelButton = QPushButton()
        self.CancelButton.setText("Отмена")
        self.OKButton = QPushButton()
        self.OKButton.setText("Сохранить")
        self.OKButton.clicked.connect(self.Finish)
        self.layout.addWidget(self.CancelButton,row, 0)
        self.layout.addWidget(self.OKButton, row, 1)

    def getDynamicComboBoxLists(self):
        return ['Var1', 'Var2', 'Var3']
    def Finish(self):
        if self.checkForFilling():
            self.accept()
        else:
            msg_box = QMessageBox()
            msg_box.setText("Заполните все поля")
            retval = msg_box.exec_()

    def createVK_UI(self):
        self.OkrugComboBox = QComboBox()
        self.OkrugComboBox.addItems(self.getDynamicComboBoxLists())
        self.VKSubjectComboBox = QComboBox()
        self.VKSubjectComboBox.addItems(self.getDynamicComboBoxLists())
        self.MunVKComboBox = QComboBox()
        self.MunVKComboBox.addItems(self.getDynamicComboBoxLists())

        self.VKComboBoxes = [self.OkrugComboBox, self.VKSubjectComboBox, self.MunVKComboBox]
        strlst = ["Округ", "СВК субъекта", "Муниципальный ВК"]
        self.VKLabels = []
        for i in strlst:
            self.VKLabels.append(QLabel(i))
        for i in range(len(strlst)):
            self.layout.addWidget(self.VKLabels[i], i + self.StaticElementsCount, 0)
            self.layout.addWidget(self.VKComboBoxes[i], i+self.StaticElementsCount, 1)
        self.addButtons( self.StaticElementsCount + len(strlst))
    def createOVU_UI(self):
        self.OkrugComboBox = QComboBox()
        self.OkrugComboBox.addItems(self.getDynamicComboBoxLists())
        self.OVUComboBoxes= [self.OkrugComboBox]
        strlst = ["Округ"]
        self.OVULabels = []
        for i in strlst:
            self.OVULabels.append(QLabel(i))
        for i in range(len(strlst)):
            self.layout.addWidget(self.OVULabels[i], i+self.StaticElementsCount,  0)
            self.layout.addWidget(self.OVUComboBoxes[i], i+self.StaticElementsCount, 1)
        self.addButtons(self.StaticElementsCount + len(strlst))
    def createVVUZ_UI(self):
        self.VVUZComboBox = QComboBox()
        self.VVUZComboBox.addItems(self.getDynamicComboBoxLists())
        self.VVUZComboBoxes = [self.VVUZComboBox]
        strlst = ["ВУЗ"]
        self.VVUZLabels = []
        for i in strlst:
            self.VVUZLabels.append(QLabel(i))
        for i in range(len(strlst)):
            self.layout.addWidget(self.VVUZLabels[i], i+self.StaticElementsCount, 0)
            self.layout.addWidget(self.VVUZComboBoxes[i], i+self.StaticElementsCount, 1)
        self.addButtons(self.StaticElementsCount + len(strlst))
    def createGUI_UI(self):
        self.addButtons(self.StaticElementsCount)
    def hide_all(self):
        try:
            self.OKButton.deleteLater()
            self.CancelButton.deleteLater()
        except:
            print('error')
        try:
            self.hide_VK()
        except:
            print('error')
        try:
            self.hide_OVU()
        except:
            print('error')
        try:
            self.hide_VVUZ()
        except:
            print('error')
    def hide_VK(self):
        lst = [self.OkrugComboBox, self.VKSubjectComboBox, self.MunVKComboBox]
        self.tryToDelete(lst)
        self.tryToDelete(self.VKLabels)
    def hide_OVU(self):
        lst = [self.OkrugComboBox]
        self.tryToDelete(lst)
        self.tryToDelete(self.OVULabels)
    def hide_VVUZ(self ):
        lst = [ self.VVUZComboBox]
        self.tryToDelete(lst)
        self.tryToDelete(self.VVUZLabels)
    def tryToDelete(self, lst:list):
        for i in lst:
            try:
                i.deleteLater()
            except:
                print("not deleted")
    def changedComboBox(self, index):
        print(self.ComboBox.currentText())
        self.hide_all()
        if self.ComboBox.currentText() == "ВК":
            self.createVK_UI()
        elif self.ComboBox.currentText() == "ОВУ":
            self.createOVU_UI()
        elif self.ComboBox.currentText() == "ВВУЗ":
            self.createVVUZ_UI()
        elif self.ComboBox.currentText() == "ГУК":
            self.createGUI_UI()
    def checkForFilling(self):
        lst = []
        for i in range(len(self.lineEdits)):
            txt = ""
            if isinstance(self.lineEdits[i], QLineEdit):
                txt = self.lineEdits[i].text()
            elif isinstance(self.lineEdits[i], QComboBox):
                txt = self.lineEdits[i].currentText()
            if(txt == ""):
                return False
        addlst = []
        if self.ComboBox.currentText() == "ВК":
            addlst = self.VKComboBoxes
        elif self.ComboBox.currentText() == "ОВУ":
            addlst = self.OVUComboBoxes
        elif self.ComboBox.currentText() == "ВВУЗ":
            addlst = self.VVUZComboBoxes
        else:
            lst = []
        for i in range(addlst):
            lst.append(addlst[i].currentText())
        return lst
    def get_data(self):
        lst = []
        for i in range(len(self.lineEdits)):
            txt = ""
            if isinstance(self.lineEdits[i], QLineEdit):
                txt = self.lineEdits[i].text()
            elif isinstance(self.lineEdits[i], QComboBox):
                txt = self.lineEdits[i].currentText()
            lst.append(txt)
        addlst = []
        if self.ComboBox.currentText() == "ВК":
            addlst = self.VKComboBoxes
        elif self.ComboBox.currentText() == "ОВУ":
            addlst = self.OVUComboBoxes
        elif self.ComboBox.currentText() == "ВВУЗ":
            addlst = self.VVUZComboBoxes
        else:
            lst = []
        for i in range(addlst):
            if (addlst[i].currentText() == ""):
                return False
        return True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(200, 300, 500, 500)
    window.setFixedSize(500, 500)
    window.show()
    sys.exit(app.exec_())
