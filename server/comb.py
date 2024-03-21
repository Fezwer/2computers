import socket
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6 import QtGui
from threading import Thread

IP = socket.gethostbyname(socket.gethostname())
PORT = 12333

class ClientListener(Thread):
    def __init__(self, signal_handler):
        super().__init__()
        self.signal_handler = signal_handler
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((IP, PORT))
        self.listener.listen(1)

    def run(self):
        connection, address = self.listener.accept()
        print('Клиент на месте')
        self.signal_handler(connection)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('img/logo.png')) 

        self.setStyleSheet('''

            QPushButton {
                line-height: 50px;
                height: 50px;
                text-align: center;
                width: 250px;
                color: #FFF;
                font-size: 20px;
                border: none;
                background-color: #8A2BE2;
                border-radius: 17px;
            }

            QPushButton::hover {
                letter-spacing: 2px;
                border-top: 1px solid rgba(255,255,255,0.5);
                border-bottom: 1px solid rgba(255,255,255,0.5);
            }
                ''')

        screen_geometry = app.primaryScreen().availableGeometry()
        self.setGeometry(screen_geometry)

        self.connection = None
        screen_geometry = app.primaryScreen().availableGeometry()

        self.layout = QVBoxLayout()
        self.pixmap = QPixmap('img/cats.jpg')
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.layout.addWidget(self.label)
        self.label.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())  # Растягиваем изображение на весь экран
        self.label.setScaledContents(True)  # Растягиваем изображение на задний фон

        button1 = QPushButton('Котики', self)
        button1.adjustSize()
        button1.clicked.connect(self.on_button_click)
        button1.move(screen_geometry.width() // 2 - button1.width() // 2, screen_geometry.height() // 2 - button1.height() // 2)

        button2 = QPushButton('Скример', self)
        button2.adjustSize()
        button2.clicked.connect(self.on_button_click_screamer)
        button2.move(screen_geometry.width() // 2 - button2.width() // 2, (screen_geometry.height() // 2 - button2.height() // 2) + 70)
        button2.setStyleSheet('background-color: #8B0000;')

        self.label_text = QLabel('Зайка, подключайся: ' + IP + ':' + str(PORT), self)
        self.label_text.setStyleSheet("color: white; font-size: 20px; font-weight: 600;")
        self.label_text.adjustSize()
        self.label_text.move(screen_geometry.width() // 2 - self.label_text.width() // 2, (screen_geometry.height() // 2 - self.label_text.height() // 2) - 70)
        self.layout.addWidget(self.label_text)

        self.setLayout(self.layout)
        self.show() 

    def on_button_click(self):
        if self.connection:
            self.connection.send("change_image".encode('utf-8'))

    def on_button_click_screamer(self):
        if self.connection:
            self.connection.send("screamer".encode('utf-8'))


app = QApplication(sys.argv)

# Создаем экземпляр окна
window = MainWindow()
window.setWindowTitle('Сервер')

def handle_connection(connection):
    window.connection = connection

# Создаем и запускаем поток для прослушивания клиентов
client_listener = ClientListener(handle_connection)
client_listener.start()

sys.exit(app.exec())