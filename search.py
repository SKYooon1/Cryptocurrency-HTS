import sys
import pyupbit
import overview
import orderbook
import gmail
import telegram

from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("search.ui", self)

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
                overview.OverviewWidget.setTicker(self.tickerGet())

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

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    sw = SearchWidget()
    sw.show()
    exit(app.exec_())