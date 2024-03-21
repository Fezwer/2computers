import socket
from PyQt6 import QtGui, QtMultimedia, QtCore, QtMultimediaWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QUrl
import pygame
from threading import Thread


class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        grad = QtGui.QLinearGradient(240, 0, 0, self.height())
        grad.setColorAt(0, QtGui.QColor(240, 200, 200))
        grad.setColorAt(1, QtGui.QColor(240, 100, 100))
        qp.fillRect(self.rect(), grad)


class ImageClient(QMainWindow): 
    def __init__(self, server_ip): 
        super().__init__() 
         
        screen_geometry = app.primaryScreen().availableGeometry() 
        self.setGeometry(screen_geometry) 
 
        self.layout = QVBoxLayout() 
        self.label = QLabel(self) 
        self.pixmap_list = [QPixmap('img/first.jpg'), QPixmap('img/second.jpg'), QPixmap('img/third.jpg'), QPixmap('img/four.jpg'), QPixmap('img/five.jpeg'), QPixmap('img/six.jpg'), 
                            QPixmap('img/seven.jpg'), QPixmap('img/eight.jpeg'), QPixmap('img/nine.jpg'), QPixmap('img/ten.jpg')]
        self.scr_list = [QPixmap('sweat_cat/sweat_cat1.png'), QPixmap('sweat_cat/sweat_cat2.png')]
        self.screamer_list = [('sweat_cat/sweat_cat1.mp3'), ('sweat_cat/sweat_cat2.mp3')]        
        self.current_index = 0 
        self.cur_index = 0
        self.label.setPixmap(self.pixmap_list[self.current_index]) 
        self.label.setGeometry(0,0,screen_geometry.width(),screen_geometry.height()) 
        self.label.setScaledContents(True) 
        self.layout.addWidget(self.label) 
 
        self.setLayout(self.layout)
        self.setWindowTitle('Мой котик успешно подключился, целую!')

        self.setWindowIcon(QtGui.QIcon('img/chmok.webp'))

        # Инициализация pygame
        pygame.mixer.init()

    def play_sound(self, sound_file):
        # Воспроизведение звука
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

 
    def change_image(self): 
        self.current_index = (self.current_index + 1) % len(self.pixmap_list) 
        self.label.setPixmap(self.pixmap_list[self.current_index]) 

    def change_image_and_sound(self):
        self.cur_index = (self.cur_index + 1) % len(self.scr_list)
        self.label.setPixmap(self.scr_list[self.cur_index])
        self.play_sound(self.screamer_list[self.cur_index])

 
class ConnectionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Привет, котик!')

        # Устанавливаем начальные размеры окна на весь экран
        screen_geometry = app.primaryScreen().availableGeometry()
        self.setGeometry(screen_geometry)

        self.central_widget = GradientWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Введите IP адрес сервера")

        self.connect_button = QPushButton("Подключиться")
        self.connect_button.clicked.connect(self.connect_to_server)

        # Устанавливаем минимальную высоту строки ввода и кнопки
        self.ip_input.setMinimumHeight(50)
        self.connect_button.setMinimumHeight(50)

        # Применяем стили для виджетов
        self.ip_input.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border-radius: 10px;")
        self.connect_button.setStyleSheet("background-color: rgba(0, 153, 255, 0.8); color: white; border-radius: 10px;")

        # Добавляем виджеты в Layout
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.connect_button)

        # Устанавливаем фокус на строку ввода при открытии окна
        self.ip_input.setFocus()

        # Устанавливаем фавиконку
        self.setWindowIcon(QtGui.QIcon('img/faviconka.jpg'))

        # Создаем переменную для хранения окна ImageClient
        self.image_client_window = None

    def connect_to_server(self):
        ip_address = self.ip_input.text()
        if not self.image_client_window:  # Создаем только один экземпляр ImageClient
            self.image_client_window = ImageClient(ip_address)
            self.image_client_window.play_sound('music/pennywise-hello_mp3cut.net.mp3')
            self.image_client_window.show()

        self.close()

        # Запускаем поток для подключения к серверу и прослушивания команд
        client_thread = Thread(target=connect_to_server, args=(ip_address, self.image_client_window))
        client_thread.start()
# Функция для подключения к серверу и прослушивания команд
def connect_to_server(server_ip, window): 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_address = (server_ip, 12333) 
    client.connect(server_address) 
 
    while True: 
        command = client.recv(1024).decode('utf-8') 
        if command == "change_image": 
            window.change_image() 
        elif command == "screamer": 
            window.change_image_and_sound()
 
app = QApplication([]) 
 
# Создаем и отображаем окно подключения 
connection_window = ConnectionWindow() 
connection_window.show() 
 
app.exec()
