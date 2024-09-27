import os
import re
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore

class M3U8Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Настройка основного окна
        self.setWindowTitle("M3U8 Downloader")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("""
            background-color: #2c3e50;
            color: #ecf0f1;
            font-family: 'Arial';
            font-size: 14px;
        """)

        # Создание элементов интерфейса
        self.url_entry = QtWidgets.QLineEdit(self)
        self.url_entry.setPlaceholderText("Введите M3U8 URL")
        self.url_entry.setStyleSheet("""
            padding: 10px;
            background-color: #34495e;
            border: 2px solid #1abc9c;
            border-radius: 5px;
            color: #ecf0f1;
        """)

        self.download_button = QtWidgets.QPushButton("Скачать", self)
        self.download_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #1abc9c;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #16a085;
            }
        """)
        self.download_button.clicked.connect(self.download)

        self.log_text = QtWidgets.QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            background-color: #34495e;
            padding: 10px;
            border: 2px solid #1abc9c;
            border-radius: 5px;
            color: #ecf0f1;
        """)

        # Лейаут для расположения элементов
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.url_entry)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_text)

        # Анимация для плавного появления окна
        self.setWindowOpacity(0)
        self.fade_in_animation = QtCore.QPropertyAnimation(self, b'windowOpacity')
        self.fade_in_animation.setDuration(1000)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.start()

    def is_valid_m3u8_url(self, url):
        valid_url_pattern = r'https?://.*\.m3u8(\?.*)?$'
        return re.match(valid_url_pattern, url) is not None

    def download(self):
        url = self.url_entry.text()
        if not self.is_valid_m3u8_url(url):
            self.log_message("Ошибка: введите корректный M3U8 URL.")
            return

        # Получение пути к текущему каталогу скрипта
        script_directory = os.path.dirname(os.path.abspath(__file__))
        vlc_executable_path = os.path.join(script_directory, "vlc.exe")

        output_file_path = os.path.join(os.path.expanduser("~"), 'Desktop', 'output.mp3')

        if not os.path.exists(vlc_executable_path):
            self.log_message(f"Ошибка: VLC не найден по пути: {vlc_executable_path}")
            return

        vlc_command = [
            vlc_executable_path,
            url,
            '--sout',
            f'#transcode{{vcodec=none, acodec=mp3}}:standard{{access=file, mux=raw, dst={output_file_path}}}',
            'vlc://quit'
        ]

        try:
            process_result = subprocess.run(vlc_command, check=True, capture_output=True, text=True)
            self.log_message(process_result.stdout)
            self.log_message(f"Успешно скачано: {output_file_path}")
        except subprocess.CalledProcessError as error:
            error_message = error.stderr.strip() if error.stderr else "Неизвестная ошибка"
            self.log_message(f"Ошибка при выполнении команды: {error_message}")

    def log_message(self, message):
        self.log_text.append(message)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Установка иконки приложения
    app_icon = QtGui.QIcon("app_icon.png")  # Замените на свой путь к иконке
    app.setWindowIcon(app_icon)

    window = M3U8Downloader()
    window.show()
    sys.exit(app.exec_())
