import sys
import pyupbit
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("search.ui", self)

        self.tickerButton.clicked.connect(self.clickTickerBtn)
        for i in pyupbit.get_tickers():
            self.listWidget.addItem(i)

    def clickTickerBtn(self):
        if self.tickerButton.text() == "검색":
            if self.getTicker.text() not in pyupbit.get_tickers():
                pass
            else:
                pass

    def setTicker(self):
        return self.ticker

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    sw = SearchWidget()
    sw.show()
    exit(app.exec_())