import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import threading
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from server.config import size, title, server_url
from server.smain import run

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, size[0], size[1])
        self.setFixedSize(size[0], size[1])
        self.setWindowIcon(QIcon('server/static/media/icon.png'))
        
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl(server_url))

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run)
    flask_thread.daemon = True
    flask_thread.start()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
