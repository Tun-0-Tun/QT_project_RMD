import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt5.QtWidgets import QLabel, QTabWidget, QPushButton, QLineEdit
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

from DictionaryModule.window import ReferencesWindow


class QMainWindowWithTabs(QMainWindow):
    def __init__(self):
        super().__init__()
        self.son_window = None
        body = {
            "Докобмен":{
                "ГУК": {
                        "Выгрузка в ГУК" : {
                            "БД": None,
                            "Изменения":None,
                            "Данные": None,
                            "Выполнить": None
                            },
                        "Загрузка из ГУК" : None
                    },
                "ОВУ_вч": {
                        "Выгрузка в ОВУ_вч" : None,
                        "Загрузка из ОВУ_вч" : None
                    },
                "ВК": {
                        "Выгрузка в ВК" : None,
                        "Загрузка из ВК" : None
                    },
                "ВУЗы": {
                        "Выгрузка в ВУЗы" : None,
                        "Загрузка из ВУЗы" : None
                    },
                "Резерв1": None,
                "Резерв2": None,
                },
            "Администрирование": None,
            "Вид": None,
            "Отчёты": None,
            }
        # Создаем QTabWidget для вкладок
        self.tab_widget = QTabWidget()
        
        layout = QVBoxLayout()

        
        layout.addWidget(self.tab_widget)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.Tab_Files()
        self.Tab_Maps()
        self.Tab_DocExch()
        self.Tab_Administration()
        
    def Tab_Files(self):
        FilesTab = QTabWidget()
        self.tab_widget.addTab(FilesTab, "Файлы")
        
    def Tab_Maps(self):
        MapsTab = QTabWidget()
        self.tab_widget.addTab(MapsTab, "Карты")
        
    def Tab_DocExch(self):
        DocExchTab = QTabWidget()
        self.tab_widget.addTab(DocExchTab, "Докобмен")

        self.Tab_DocExch_References(DocExchTab)
        self.Tab_DocExch_StatePersonnelManagement(DocExchTab)

    def Tab_DocExch_References(self, DocExchTab):
        GuideTab = QWidget()
        DocExchTab.addTab(GuideTab, "Справочники")

        layout1 = QHBoxLayout(GuideTab)
        GuideTab.setMinimumHeight(50)
        GuideTab.setMaximumHeight(50)
        
        self.Tab_DocExch_References_Button(layout1)
         
    def Tab_DocExch_References_Button(self, layout1):
        button = QPushButton("Загрузка")
        layout1.addWidget(button)
        button.clicked.connect(self.GlobalOpen(LoadingWindow))

        button = QPushButton("Обновление")
        layout1.addWidget(button)
        button.clicked.connect(lambda: ReferencesWindow().show())
        
        button = QPushButton("Предложения")
        layout1.addWidget(button)
        button.clicked.connect(self.GlobalOpen(OfferWindow))
        
    def Tab_Administration(self):
        AdministrationTab = QTabWidget()
        self.tab_widget.addTab(AdministrationTab, "Администрирование")

    def Tab_DocExch_StatePersonnelManagement(self, DocExchTab):
        GuideTab = QWidget()
        DocExchTab.addTab(GuideTab, "ГУК")

        layout1 = QHBoxLayout(GuideTab)
        GuideTab.setMinimumHeight(50)
        GuideTab.setMaximumHeight(50)
        
        self.Tab_DocExch_StatePersonnelManagement_Button(layout1)
        
    def Tab_DocExch_StatePersonnelManagement_Button(self, layout1):
        button = QPushButton("Выгрузка")
        layout1.addWidget(button)
        button.clicked.connect(self.GlobalOpen(DischargeWindow))

        button = QPushButton("Обновление")
        layout1.addWidget(button)
        button.clicked.connect(lambda: ReferencesWindow().show())
        
        button = QPushButton("Предложения")
        layout1.addWidget(button)
        button.clicked.connect(self.GlobalOpen(OfferWindow))
    def GlobalOpen(self, Form):
        def func():
            self.son_window = Form(self)
            self.son_window.show()
        return func

class QSmallWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setGeometry(200, 300, 400, 100)
        self.setWindowModality(2)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
        
    def open_file_dialog(self):
        # Открываем диалоговое окно обзора файлов
        file_dialog = QFileDialog()
        file_dialog.setWindowTitle("Выберите файл")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text files (*.csv);;All files (*)")

        if file_dialog.exec_():
            # Получаем выбранный файл
            selected_files = file_dialog.selectedFiles()
            self.text_box.setText(selected_files[0])

class LoadingWindow(QSmallWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Загрузка")
        
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        path_button = QPushButton("Обзор")
        self.text_box = QLineEdit("C:\\Users\\PC\\Documents", self)
        layout1.addWidget(self.text_box)
        layout1.addWidget(path_button)
        path_button.clicked.connect(self.open_file_dialog)

        execute_button = QPushButton("Выполнить")
        layout2.addWidget(execute_button)
        execute_button.setStyleSheet("background-color: #80FF80;")#Зелёный
        execute_button.clicked.connect(lambda: None)
        
        cancel_button = QPushButton("Отмена")
        layout2.addWidget(cancel_button)
        cancel_button.setStyleSheet("background-color: #FF8080;")#Красный
        cancel_button.clicked.connect(self.CloseWindow)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def CloseWindow(self):
        self.deleteLater()
        
class OfferWindow(QSmallWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Предложение")
        
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        path_button = QPushButton("Обзор")
        self.text_box = QLineEdit("C:\\Users\\PC\\Documents", self)
        layout1.addWidget(self.text_box)
        layout1.addWidget(path_button)
        path_button.clicked.connect(self.open_file_dialog)

        execute_button = QPushButton("Выполнить")
        layout2.addWidget(execute_button)
        execute_button.setStyleSheet("background-color: #80FF80;")#Зелёный
        execute_button.clicked.connect(lambda: None)
        
        cancel_button = QPushButton("Отмена")
        layout2.addWidget(cancel_button)
        cancel_button.setStyleSheet("background-color: #FF8080;")#Красный
        cancel_button.clicked.connect(self.CloseWindow)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def CloseWindow(self):
        self.deleteLater()

class DischargeWindow(QSmallWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Выгрузка из ГУК")
        
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        '''
        path_button = QPushButton("Обзор")
        self.text_box = QLineEdit("C:\\Users\\PC\\Documents", self)
        layout1.addWidget(self.text_box)
        layout1.addWidget(path_button)
        path_button.clicked.connect(self.open_file_dialog)

        execute_button = QPushButton("Выполнить")
        layout2.addWidget(execute_button)
        execute_button.setStyleSheet("background-color: #80FF80;")#Зелёный
        execute_button.clicked.connect(lambda: None)
        
        cancel_button = QPushButton("Отмена")
        layout2.addWidget(cancel_button)
        cancel_button.setStyleSheet("background-color: #FF8080;")#Красный
        cancel_button.clicked.connect(self.CloseWindow)
        '''
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
    def CloseWindow(self):
        self.deleteLater()

''' Unused
class Update(QSmallWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Обновление")

        layout = QVBoxLayout()
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)

        path_button = QPushButton("Путь к файлу")
        layout1.addWidget(path_button)
        path_button.clicked.connect(lambda: None)

        execute_button = QPushButton("Выполнить")
        layout2.addWidget(execute_button)
        execute_button.setStyleSheet("background-color: #80FF80;")#Зелёный
        execute_button.clicked.connect(lambda: None)
        
        cancel_button = QPushButton("Отмена")
        layout2.addWidget(cancel_button)
        cancel_button.setStyleSheet("background-color: #FF8080;")#Красный
        cancel_button.clicked.connect(lambda: self.close())
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
'''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindowWithTabs()
    window.setGeometry(200, 300, 600, 500)
    window.show()
    sys.exit(app.exec_())
