import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtWidgets import QHBoxLayout,QVBoxLayout
from PyQt5.QtWidgets import QLabel, QTabWidget
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QMenu, QAction

class QMainWindowWithTabs(QMainWindow):
    def __init__(self):
        super().__init__()
        body = {
                "Справочники": {
                        "Загрузка": None,
                        "Обновление": {
                                "Путь к файлу": None,
                                "Выполнить": None,
                                "Отмена": None
                            },
                        "Предложения": {
                                "ВУЗы": None,
                                "Категория": None,
                                "Выполнить": None
                            }
                        
                    },
                "ГУК": {
                        "Выгрузка в ГУК" : None,
                        "Загрузка из ГУК" : None
                    },
                "ОВУ_вч": {
                        "Выгрузка в ОВУ_вч" : None,
                        "Загрузка из ОВУ_вч" : None
                    },
                "ВК": {
                        "Выгрузка в ВК" : None,
                        "Загрузка из ВК" : None
                    }
            }
        for key1 in body:
            # Создаем меню <key1>
            file_menu = self.menuBar().addMenu(key1)
            body2 = body[key1]
            if body2 is None:
                #file_menu.triggered.connect(lambda: self.action(key1))
                continue
            # Создаем действие <key2>
            for key2 in body2:
                key2_action = QAction(key2, self)
                file_menu.addAction(key2_action)
                body3 = body2[key2]
                if body3 is None:
                    #file_menu.triggered.connect(lambda: self.action(key1))
                    continue
                # Создаем подменю для действия <key2>
                key2_submenu = QMenu()
                key2_action.setMenu(key2_submenu)
                for key3 in body3:
                    # Добавляем действия <key3> в подменю
                    key3_action = QAction(key3, self)
                    key2_submenu.addAction(key3_action)
                    #Соединяем сигналы со слотами
                    key3_action.triggered.connect(self.action(key3))
        
        
    def action(self, doing):
        string = doing
        def f():
            print(string)
            return
        return f


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindowWithTabs()
    window.setGeometry(200, 300, 500, 500)
    window.show()
    sys.exit(app.exec_())
