import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Обычные вкладки")
        self.setGeometry(100, 100, 400, 300)

        # Создаем виджет вкладок
        tab_widget = QTabWidget()
        self.setCentralWidget(tab_widget)

        # Создаем вкладки
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Добавляем вкладки на виджет вкладок
        tab_widget.addTab(tab1, "Вкладка 1")
        tab_widget.addTab(tab2, "Вкладка 2")
        tab_widget.addTab(tab3, "Вкладка 3")

        # Наполняем каждую вкладку содержимым
        layout_tab1 = QVBoxLayout()
        button_tab1 = QPushButton("Кнопка на вкладке 1")
        layout_tab1.addWidget(button_tab1)
        tab1.setLayout(layout_tab1)

        layout_tab2 = QVBoxLayout()
        button_tab2 = QPushButton("Кнопка на вкладке 2")
        layout_tab2.addWidget(button_tab2)
        tab2.setLayout(layout_tab2)

        layout_tab3 = QVBoxLayout()
        button_tab3 = QPushButton("Кнопка на вкладке 3")
        layout_tab3.addWidget(button_tab3)
        tab3.setLayout(layout_tab3)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
