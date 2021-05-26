import sys
import pyupbit
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidgetItem, QProgressBar, QWidget, QApplication, QMainWindow
from PyQt5.QtCore import Qt, QThread, pyqtSignal

class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("search.ui", self)

    def clickTickerBtn(self):
        if self.tickerButton.text() == "검색":
            if self.getTicker.text not in pyupbit.get_tickers():
                self.textEdit.append("올바른 티커가 아닙니다.")
            else:
                self.ticker = self.getTicker.text()
        return self.ticker

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sw = SearchWidget()
    sw.show()
    exit(app.exec_())