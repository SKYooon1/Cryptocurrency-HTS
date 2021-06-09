import sys
import pyupbit
import gmail
import telegram
from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow
import overview

form_class = uic.loadUiType("main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.tickerButton.clicked.connect(self.clickTickerBtn)
        self.listWidget.itemDoubleClicked.connect(self.itemSelect)

        self.gmailButton.clicked.connect(self.clickGmailBtn)
        self.gmailButton.setIcon(QtGui.QIcon('gmail.png'))
        self.gmailButton.setIconSize(QtCore.QSize(24, 24))

        self.teleButton.clicked.connect(self.clickTeleBtn)
        self.teleButton.setIcon(QtGui.QIcon('telegram.png'))
        self.teleButton.setIconSize(QtCore.QSize(24, 24))

        self.tickerList = []
        for i in pyupbit.get_tickers(fiat="KRW"):
            self.tickerList.append(i.split('-')[1])
        for i in self.tickerList:
            self.listWidget.addItem(i)

    def clickTickerBtn(self):
        if self.tickerButton.text() == "검색":
            if self.getTicker.text() not in self.tickerList:
                wrongName = QMessageBox()
                wrongName.setText("없는코인")
                wrongName.setStandardButtons(QMessageBox.Yes)
                wrongName = wrongName.exec()
            else:
                overview.OVTICKER = self.tickerGet()

    def clickGmailBtn(self):
        if self.gmailButton.text() == "Gmail":
            gmail.sendMail(self.getTicker.text())        # 티커의 현재가만 발송하도록 되어있음
            notify = QMessageBox()
            notify.setText("메일 발송 완료")
            notify.setStandardButtons(QMessageBox.Yes)
            notify = notify.exec()

    def clickTeleBtn(self):
        if self.teleButton.text() == "Telegram":
            telegram.send(self.getTicker.text())   # 티커의 현재가만 발송하도록 되어있음
            notify = QMessageBox()
            notify.setText("텔레그램 봇 메세지 발송")
            notify.setStandardButtons(QMessageBox.Yes)
            notify = notify.exec()

    def itemSelect(self):
        lst_item = self.listWidget.selectedItems()
        for item in lst_item:
            self.getTicker.setText(item.text())

    def tickerGet(self):
        return self.getTicker.text()

    def closeEvent(self, event):
        self.widget_2.closeEvent(event)
        self.widget_3.closeEvent(event)
        self.widget_4.closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())