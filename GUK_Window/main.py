import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QFileDialog, QLabel, QGridLayout, QLineEdit, QComboBox, QAbstractItemView, QMessageBox
from PyQt5.QtGui import QColor

class Participant:
    def __init__(self, id, rang, sex, surname, name, fathername, birthday, contacts, status, quota, graduated, district, subject, vkSelection, university, registrDate, selectionCriteria, educationCenterDate, documentNumber, note):
        self.id = id
        self.rang = rang
        self.sex = sex
        self.surname = surname
        self.name = name
        self.fathername = fathername
        self.birthday = birthday
        self.contacts = contacts
        self.status = status
        self.quota = quota
        self.graduated = graduated
        self.district = district
        self.subject = subject
        self.vkSelection = vkSelection
        self.university = university
        self.regitsrDate= registrDate
        self.selectionCriteria, self.educationCenterDate, self.documentNumber, self.note =selectionCriteria, educationCenterDate, documentNumber, note
        self.stringList = [id, rang, sex, surname, name, fathername, birthday, contacts, status, quota, graduated, district, subject, vkSelection, university, registrDate, selectionCriteria, educationCenterDate, documentNumber, note]
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

        self.setWindowTitle('Главное окно')

        self.table_settings()


        self.add_row_button = QPushButton('Редактировать строку')
        self.add_row_button.clicked.connect(self.add_row)
        self.table.selectedItems()

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

#table settings region
    def table_settings(self):
        self.table = QTableWidget()
        self.column_names = [
            "ID",
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
            "Примечание",
            "Резервная_1",
            "Резервная_2",
            "Резервная_3",
            "Резервная_4",
            "Резервная_5"
        ]
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
    def add_row(self):
        student = self.get_selected_row()
        if len(student) == 0:
            return
        self.SELECTED_INDEX = int(student[0])
        student = student[1:]
        print(student)
        dialog = EditRowDialog(student)
        if dialog.exec_():
            data = dialog.get_data()
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for i, item in enumerate(data):
                self.table.setItem(row_position, i, QTableWidgetItem(item))
            self.set_column_color(1, QColor('blue'))  # второй столбец
            self.set_column_color(2, QColor('blue'))
    def get_selected_row(self):
        values = []
        if len(self.table.selectedItems()) == 0:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText('Ни одна строка не выделена')
            msg_box.setStandardButtons(QMessageBox.Ok)
            retval = msg_box.exec_()

            return values
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