import datetime

import requests
from PyQt5 import QtWidgets, QtCore
import clientui


class Window(QtWidgets.QMainWindow, clientui.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.pressed.connect(self.send_message)

        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get_messages)
        self.timer.start(1000)

    def get_messages(self):
        try:
            response = requests.get('http://127.0.0.1:5000/messages',
                                    params={'after': self.after})
        except:
            return
        response_data = response.json()

        for message in response_data['messages']:
            self.print_messages(message)
            self.after = message['time']

    def print_messages(self, message):
        beauty_time = datetime.datetime.fromtimestamp(message['time'])
        beauty_time = beauty_time.strftime('%Y/%m/%d %H:%M')
        self.textBrowser.append(f'{beauty_time}, {message["name"]}')
        self.textBrowser.append(f'{message["text"]}')
        self.textBrowser.append('')

    def send_message(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()

        try:
            response = requests.post('http://127.0.0.1:5000/send', json={
                'name': name,
                'text': text
            })
        except:
            self.textBrowser.append('No connection')
            self.textBrowser.append('')
            return

        if response.status_code != 200:
            self.textBrowser.append('Name or text are empty')
            self.textBrowser.append('')
            return

        self.textEdit.clear()


app = QtWidgets.QApplication([])
window = Window()
window.show()
app.exec_()
