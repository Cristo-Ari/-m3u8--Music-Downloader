import os
import re
import subprocess
from PyQt5 import QtWidgets

class M3U8Downloader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("M3U8 Downloader")
        self.setGeometry(100, 100, 500, 400)

        self.url_entry = QtWidgets.QLineEdit(self)
        self.url_entry.setPlaceholderText("Введите M3U8 URL")

        self.download_button = QtWidgets.QPushButton("Скачать", self)
        self.download_button.clicked.connect(self.download)

        self.log_text = QtWidgets.QTextEdit(self)
        self.log_text.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.url_entry)
        layout.addWidget(self.download_button)
        layout.addWidget(self.log_text)

    def is_valid_m3u8_url(self, url):
        return re.match(r'https?://.*\.m3u8(\?.*)?$', url) is not None

    def download(self):
        url = self.url_entry.text()
        if not self.is_valid_m3u8_url(url):
            self.log("Ошибка: введите корректный M3U8 URL.")
            return

        output_file = os.path.join(os.path.expanduser("~"), 'Desktop', 'output.mp3')
        vlc_path = os.path.join(os.getcwd(), "vlc.exe")

        if not os.path.exists(vlc_path):
            self.log(f"Ошибка: VLC не найден по пути: {vlc_path}")
            return

        vlc_command = [
            vlc_path,
            url,
            '--sout',
            f'#transcode{{vcodec=none, acodec=mp3}}:standard{{access=file, mux=raw, dst={output_file}}}',
            'vlc://quit'
        ]

        try:
            result = subprocess.run(vlc_command, check=True, capture_output=True, text=True)
            self.log(result.stdout)
            self.log(f"Успешно скачано: {output_file}")
        except subprocess.CalledProcessError as e:
            error_message = e.stderr.strip() if e.stderr else "Неизвестная ошибка"
            self.log(f"Ошибка при выполнении команды: {error_message}")

    def log(self, message):
        self.log_text.append(message)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = M3U8Downloader()
    window.show()
    sys.exit(app.exec_())
