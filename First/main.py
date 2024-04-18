import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QFileDialog, QLabel, QGridLayout, QLineEdit, QComboBox, QAbstractItemView, \
    QCalendarWidget
from PyQt5.QtGui import QColor
from StaticResources import TableData
class AddRowDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Добавление строки')

        self.column_names = TableData.getShortTableRows()

        layout = QGridLayout()

        self.labels = []
        self.line_edits = []
        for i in range(1, len(self.column_names)):

            cur_name = self.column_names[i]
            label = QLabel(cur_name, self)
            if cur_name in TableData.getRussianColumnNames().keys():
                combo_box = QComboBox(self)
                lst = TableData.getColumnValues()[TableData.getRussianColumnNames()[cur_name]]
                combo_box.addItems(lst)
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
            elif cur_name == 'Число, год рождения':
                calendar = QCalendarWidget(self)
                self.labels.append(label)
                self.line_edits.append(calendar)
                layout.addWidget(label, i, 0)
                layout.addWidget(calendar, i, 1)
            else:
                line_edit = QLineEdit(self)
                self.labels.append(label)
                self.line_edits.append(line_edit)

                layout.addWidget(label, i, 0)
                layout.addWidget(line_edit, i, 1)

        self.add_button = QPushButton('Добавить', self)
        self.add_button.clicked.connect(self.accept)

        layout.addWidget(self.add_button, 10, 0, 1, 2)

        self.setLayout(layout)

    def get_data(self):
        lst = []
        for inp in self.line_edits:
            if isinstance(inp, QComboBox):
                lst.append(inp.currentText())
            elif isinstance(inp, QCalendarWidget):
                lst.append(inp.selectedDate().toString("dd-MM-yyyy"))
            else:
                lst.append(inp.text())
        return lst
        #return [input.currentText() if isinstance(input, QComboBox) else input.text() for input in self.line_edits]



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.design_set()
        self.db()
        self.update_table_view()

    #DESIGN SETTINGS
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

        self.add_row_button = QPushButton('Добавить строку')
        self.add_row_button.clicked.connect(self.add_row)

        self.export_button = QPushButton('Экспорт в CSV')
        self.export_button.clicked.connect(self.export_csv)

        self.import_button = QPushButton('Импорт из CSV')
        self.import_button.clicked.connect(self.import_csv)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.table)
        layout.addWidget(self.add_row_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.import_button)

        self.setCentralWidget(central_widget)
    #DB
    def db(self):
        connection = sqlite3.connect('Students_db.db')
        connection.close()
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect('Students_db.db')
        cursor = connection.cursor()
        cursor.execute('''
           CREATE TABLE IF NOT EXISTS Students (
           ID PRIMARY KEY,
           PersonalNumber INTEGER,
           Rang TEXT,
           Sex TEXT NOT NULL,
           Surname TEXT NOT NULL,
           Name TEXT NOT NULL,
           FatherName TEXT,
           Birthday TEXT NOT NULL,
           Contacts TEXT NOT NULL,
           Status  TEXT,
           SeparateQuota TEXT,
           Graduated BOOL NOT NULL,
           District TEXT NOT NULL,
           Subject TEXT NOT NULL,
           VK TEXT NOT NULL,
           University TEXT, 
           RegistrationDate TEXT NOT NULL,
           SelectionCriteria TEXT NOT NULL,
           ReferalDate TEXT NOT NULL,
           DocumentNumber TEXT NOT NULL,
           Note TEXT,
           ADD1, 
           ADD2,
           ADD3,
           ADD4,
           ADD5)''')
        connection.commit()
        connection.close()
        #lst = ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '', '1', 'Вариант 1', 'Вариант 1', 'Вариант 1', 'Вариант 1', 'Вариант 1', 'Вариант 1', 'Вариант 1', 'Вариант 1', 'Вариант 1', '0', '0', '0', '0', '0']
        #self.add_student(lst)\
    def get_table_rows_count(self):
        connection = sqlite3.connect('Students_db.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM  Students")
        res = len(cursor.fetchall())
        cursor.close()
        connection.close()
        return res
    def add_student(self, list):
        connection = sqlite3.connect('Students_db.db')
        cursor = connection.cursor()

        for i in range(len(list)):
            if i != 1:
                list[i] = "'" + list[i] + "'"
        # Добавляем нового пользователя
        params = ''
        for s in list:
            params += s + ','
        params = params[0:len(params)-1]
        print(params)
        columns = 'ID, PersonalNumber, Rang, Sex, Surname, Name, FatherName, Birthday, Contacts, Status, SeparateQuota, Graduated, District, Subject, VK, University, RegistrationDate,SelectionCriteria, ReferalDate, DocumentNumber, Note, ADD1, ADD2, ADD3, ADD4, ADD5'
        cursor.execute(f'INSERT INTO Students ({columns}) VALUES ({params})')
        # Сохраняем изменения и закрываем соединение
        connection.commit()
        connection.close()

    def get_db_rows(self) -> list:
        connection = sqlite3.connect('Students_db.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM  Students")
        res = cursor.fetchall()
        cursor.close()
        connection.close()
        return res
    #FUNCTIONS

    def update_table_view(self):
        self.table.clear()
        records = self.get_db_rows()
        for i in range(len(records)):
            self.add_row_from_db(i, records[i])
    def add_row_from_db(self, row_number:int, lst:list):
        self.table.insertRow(row_number)
        for i in range(len(lst)):
            self.table.setItem(row_number, i, QTableWidgetItem(str(lst[i])))
    def add_row(self):
        dialog = AddRowDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            id = self.get_table_rows_count()
            data.insert(0, str(id))
            print(data)
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for i, item in enumerate(data):
                self.table.setItem(row_position, i, QTableWidgetItem(item))
            for i in range(5): #additional columns
                self.table.setItem(row_position, self.table.columnCount() - i - 1, QTableWidgetItem(""))

            lst = data
            for i in range(5):
                lst.append("0")
            print(lst)
            self.add_student(lst)
            self.set_column_color(1, QColor('blue'))  # второй столбец
            self.set_column_color(2, QColor('blue'))
    def export_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'w') as file:
                for row in range(self.table.rowCount()):
                    line = ','.join([
                        self.table.item(row, column).text() for column in range(self.table.columnCount() )
                    ])
                    file.write(line + '\n')
    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл CSV", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, 'r') as file:
                data = file.readlines()
                #self.table.setRowCount(0)  # очищаем таблицу перед загрузкой новых данных
                for line in data:
                    row_data = line.strip().split(',')
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    for i, item in enumerate(row_data):
                        self.table.setItem(row_position, i, QTableWidgetItem(item))
                self.set_column_color(3, QColor('blue'))  # второй столбец
                self.set_column_color(4, QColor('blue'))

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