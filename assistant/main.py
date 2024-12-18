import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from server.config import size, title, server_url
from server.smain import run
import threading
import logging

# Отключаем все сообщения логгера
logging.getLogger().setLevel(logging.CRITICAL)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, size[0], size[1])
        self.setFixedSize(size[0], size[1])
        self.setWindowIcon(QIcon('server/static/media/icon.jpg'))

        # Создаем веб-браузер
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.browser.setUrl(QUrl(server_url))

        # Привязываем событие загрузки страницы к кастомизации стилей
        self.browser.page().loadFinished.connect(self.add_custom_scrollbar_styles)

    def add_custom_scrollbar_styles(self):
        self.browser.page().runJavaScript("""
            const style = document.createElement('style');
            style.innerHTML = `
                ::-webkit-scrollbar {
                    width: 8px; /* Толщина вертикальной полосы */
                    height: 8px; /* Высота горизонтальной полосы */
                }
                ::-webkit-scrollbar-thumb {
                    background: #7c2fc4; /* Цвет движущейся части */
                    border-radius: 4px; /* Закругленные края */
                }
                ::-webkit-scrollbar-thumb:hover {
                    background: #ff0088; /* Цвет при наведении */
                }
                ::-webkit-scrollbar-track {
                    background: #000; /* Цвет фона полосы */
                }
            `;
            document.head.appendChild(style);
        """)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=run, daemon=True)
    app = QApplication(sys.argv)
    window = MainWindow()
    flask_thread.start()
    window.show()
    sys.exit(app.exec_())
