import sys
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTableWidget, \
    QTableWidgetItem, QDialog, QFileDialog, QLabel, QGridLayout, QLineEdit, QComboBox, QAbstractItemView
from PyQt5.QtGui import QColor
from StaticResources import TableData
class AddRowDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Добавление строки')

        self.column_names = [
            "id",
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
        for i in range(1, len(self.column_names)):

            cur_name = self.column_names[i]
            label = QLabel(cur_name, self)
            if cur_name == 'Округ' or i > 14:
                combo_box = QComboBox(self)
                combo_box.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
            elif cur_name == 'Субъект':
                combo_box = QComboBox(self)
                combo_box.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
            elif cur_name == 'Выбор ВК':
                combo_box = QComboBox(self)
                combo_box.addItems(["Вариант 1", "Вариант 2", "Вариант 3"])
                self.labels.append(label)
                self.line_edits.append(combo_box)
                layout.addWidget(label, i, 0)
                layout.addWidget(combo_box, i, 1)
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
        return [input.currentText() if isinstance(input, QComboBox) else input.text() for input in self.line_edits]



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.design_set()

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
    #FUNCTIONS
    def add_row(self):
        dialog = AddRowDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            id = self.table.rowCount()
            data.insert(0, str(id))
            print(data)
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for i, item in enumerate(data):
                self.table.setItem(row_position, i, QTableWidgetItem(item))

            for i in range(5): #additional columns
                self.table.setItem(row_position, self.table.columnCount() - i - 1, QTableWidgetItem(""))

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