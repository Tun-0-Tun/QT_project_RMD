import sys

import sqlite3

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QFileDialog, QLabel, QGridLayout, QLineEdit, QComboBox, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QColor

import MyQTWidgets.checkableComboBox
import MyQTWidgets.CheckableComboBoxesList
from MyQTWidgets import checkableComboBox
from PyQt5.uic.properties import QtWidgets


from StaticResources import TableData

class EditRowDialog(QDialog):
    def __init__(self, student):
        super().__init__(None)

        self.setWindowTitle('Изменение строки')

        self.column_names = [
            "личный номер (при наличии)",
            "в/зв по запасу (при наличии)",
            "Пол",
            "Фамилия",
            "Имя",
            "Отчество",
            "Число, год рождения",
            "Контакты (тел. адррес эл. почты)",
            "Статус",
            "Отдельная квота",
            "Выпускник СВУ, ПКУ, КК Минобороны",
            "Округ",
            "Субъект",
            "Выбор ВК",
            "Наименование вуза",
            "Дата регистрации заявления",
            "Признак отбора",
            "Дата направления учебного центра",
            "Исходящий номер документа",
            "Примечание"
        ]

        layout = QGridLayout()

        self.labels = []
        self.line_edits = []

        print('Building columns')
        for i in range(len(self.column_names)):
            cur_name = self.column_names[i]
            label = QLabel(cur_name, self)
            label.text = student[i]
            if cur_name == 'Округ' or i > 13:
                combo_box = QComboBox(self)
                combo_box.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])
                combo_box.setCurrentText(student[i])
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
            elif cur_name == 'Субъект':
                combo_box = QComboBox(self)
                combo_box.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])
                combo_box.setCurrentText(student[i])
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
            elif cur_name == 'Выбор ВК':
                combo_box = QComboBox(self)
                combo_box.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])
                combo_box.setCurrentText(student[i])
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
            else:
                line_edit = QLineEdit(self)
                line_edit.setText(student[i])
                self.labels.append(label)
                self.line_edits.append(line_edit)

                layout.addWidget(label, i, 0)
                layout.addWidget(line_edit, i, 1)

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.accept)

        layout.addWidget(self.add_button, 10, 0, 1, 2)

        self.setLayout(layout)

    def get_data(self):
        return [input.currentText() if isinstance(input, QComboBox) else input.text() for input in self.line_edits]



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.design_set()
        self.db()
        self.update_table_view()

    #FORM DESIGN
    def table_settings(self):
        self.table = QTableWidget()
        self.column_names =  TableData.getTableRows()
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
    def design_set(self):
        self.setWindowTitle('Главное окно')

        self.table_settings()

        self.add_row_button = QPushButton('Редактировать строку')
        self.add_row_button.clicked.connect(self.add_row)
        self.table.selectedItems()

        self.export_button = QPushButton('Экспорт в CSV')
        self.export_button.clicked.connect(self.export_csv)

        self.import_button = QPushButton('Импорт из CSV')
        self.import_button.clicked.connect(self.import_csv)
        self.checkable_combobox_list = MyQTWidgets.CheckableComboBoxesList.MyWidget(self)
        self.checkable_combobox_list.setGeometry(200, 150, 150, 30)
        self.checkable_combobox_list.createComboBoxes(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.checkable_combobox_list)
        layout.addWidget(self.table)
        layout.addWidget(self.add_row_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.import_button)

        self.setCentralWidget(central_widget)

    #DataBase
    def db(self):
        connection = sqlite3.connect('GUK_MAIN_DB.db')
        connection.close()
        self.create_table()
    def create_table(self):
        connection = sqlite3.connect('GUK_MAIN_DB.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Students (
        ID  PRIMARY KEY,
        PersonalNumber INTEGER,
        Rang TEXT,
        Sex TEXT NOT NULL,
        Surname TEXT NOT NULL,
        Name TEXT NOT NULL,
        FatherName TEXT,
        Birthday DATETIME NOT NULL,
        Contacts TEXT NOT NULL,
        Status  TEXT,
        SeparateQuota TEXT,
        Graduated BOOL NOT NULL,
        District TEXT NOT NULL,
        Subject TEXT NOT NULL,
        VK TEXT NOT NULL,
        University TEXT, 
        RegistrationDate DATETIME NOT NULL,
        SelectionCriteria TEXT NOT NULL,
        ReferalDate DATETIME NOT NULL,
        DocumentNumber TEXT NOT NULL,
        Note TEXT,
        ADD1, 
        ADD2,
        ADD3,
        ADD4,
        ADD5)''')
        connection.commit()
        connection.close()
    def sql_request_organizer(self):
        connection = sqlite3.connect('GUK_MAIN_DB.db')
        cursor = connection.cursor()
        keys = self.checkable_combobox_list.TotalDict.keys()
        request = ''
        for k in keys:
            request += self.sql_request(cursor,k, self.checkable_combobox_list.TotalDict[k]) + ','
        request = request[0:len(request) -1]
        #cursor.execute(f"SELECT * FROM Students ({request})")
        cursor.execute(f"SELECT * FROM Students")
        records = cursor.fetchall()
        print(records)
        connection.commit()
        connection.close()
        return records
    def sql_request(self, cursor, columnName, valuesList):
        values = ''
        for l in valuesList:
            if columnName != 'PersonalNumber':
                values += "'"+ l +"'" + ","
            else:
                values += l +","
        values = values[0:len(values)-1]
        res = f'WHERE {columnName} IN ({values})'
        return res

    def add_record(self, list:list):
        try:
            connection = sqlite3.connect('GUK_MAIN_DB.db')
            cursor = connection.cursor()

            for i in range(len(list)):
                if i != 1:
                    list[i] = "'" + list[i] + "'"
            # Добавляем нового пользователя
            params = ''
            for s in list:
                params += s + ','
            params = params[0:len(params) - 1]
            columns = 'ID, PersonalNumber, Rang, Sex, Surname, Name, FatherName, Birthday, Contacts, Status, SeparateQuota, Graduated, District, Subject, VK, University, RegistrationDate,SelectionCriteria, ReferalDate, DocumentNumber, Note, ADD1, ADD2, ADD3, ADD4, ADD5'
            cursor.execute(f'INSERT INTO Students ({columns}) VALUES ({params})')
            # Сохраняем изменения и закрываем соединение
            connection.commit()
            connection.close()
        except:
            print("Error occured")
    #def add_record(self, string:str):
    ##    connection = sqlite3.connect('GUK_MAIN_DB.db')
     #   cursor = connection.cursor()
     #   columns = 'ID, PersonalNumber, Rang, Sex, Surname, Name, FatherName, Birthday, Contacts, Status, SeparateQuota, Graduated, District, Subject, VK, University, RegistrationDate,SelectionCriteria, ReferalDate, DocumentNumber, Note, ADD1, ADD2, ADD3, ADD4, ADD5'
     #   cursor.execute(f'INSERT INTO Students ({columns}) VALUES ({string})')
     #   # Сохраняем изменения и закрываем соединение
     #   connection.commit()
     #   connection.close()
    # FUNCTIONS
    def update_table_view(self):
        self.table.clear()
        records = self.sql_request_organizer()
        for i in range(len(records)):
            self.add_row_from_db(i, records[i])

    def add_row_from_db(self, row_number, lst):
        self.table.insertRow(row_number)
        for i in range(len(lst)):
            self.table.setItem(row_number, i, QTableWidgetItem(str(lst[i])))
    def add_row(self):
        #...
        try:
            self.checkable_combobox_list.getChosenValues()
            print(self.checkable_combobox_list.TotalDict)
            #...
            student = self.get_selected_row()
            if len(student) == 0:
                return
            id = student[0]
            student = student[1:]
            dialog = EditRowDialog(student)
            if dialog.exec_():
                data = dialog.get_data()
                data.insert(0, str(id))
                row_position = self.SELECTED_INDEX # ищем строку с нужным номером
                for i, item in enumerate(data):
                    self.table.setItem(row_position, i, QTableWidgetItem(item))
                self.set_column_color(1, QColor('blue'))  # второй столбец
                self.set_column_color(2, QColor('blue'))
        except:
            print("error occured")
    def get_selected_row(self):
        values = []
        if len(self.table.selectedItems()) == 0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText('Ни одна строка не выделена')
            msg_box.setStandardButtons(QMessageBox.Ok)
            retval = msg_box.exec_()

            return values
        self.SELECTED_INDEX = int(self.table.selectedItems()[0].row())
        for selected_item in self.table.selectedItems():
            # create [item from col 0, item from col 1]
            values.insert(selected_item.column(), selected_item.text())
        return values



    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w') as file:
                for row in range(self.table.rowCount()):
                    line = ','.join([self.table.item(row, column).text() for column in range(self.table.columnCount())])
                    file.write(line + '\n')

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'r') as file:
                data = file.readlines()
                #self.table.setRowCount(0)  # очищаем таблицу перед загрузкой новых данных
                for line in data:
                    line_edited = line[0: len(line) -1] # to remove \n at the end
                    row_data = line_edited.split(',')
                    self.add_record(row_data)
                self.update_table_view()

    def set_column_color(self, column, color):
        for row in range(self.table.rowCount()):
            item = self.table.item(row, column)
            if item is not None:
                item.setBackground(color)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(200, 300, 2000, 750)
    window.show()
    sys.exit(app.exec_())