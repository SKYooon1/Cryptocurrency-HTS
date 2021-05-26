import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from pyupbit import WebSocketManager
from PyQt5.QtCore import QThread, pyqtSignal

class OverViewWorker(QThread):
    dataSent = pyqtSignal(int, float, float, int, float, int, float, float, int)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.running = True

    def run(self):
        wm = WebSocketManager("ticker", [f"{self.ticker}"])
        while self.running:
            data = wm.get()
            self.dataSent.emit(int  (data['trade_price']),
                               float(data['change_rate']),
                               float(data['acc_trade_volume_24h']),
                               int  (data['high_price']),
                               float(data['acc_trade_price_24h']),
                               int  (data['low_price']),
                               float(data['acc_ask_volume']),
                               float(data['acc_bid_volume']),
                               int  (data['prev_closing_price']))

    def close(self):
        self.running = False

class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-BTC"):
        super().__init__(parent)
        uic.loadUi("overview.ui", self)
        self.ticker = ticker.replace("KRW-", "")

        self.ovw = OverViewWorker(ticker)
        self.ovw.dataSent.connect(self.fillData)
        self.ovw.start()

    def fillData(self, currPrice, chgRate, volume, highPrice, value,
                 lowPrice, askVolume, bidVolume, prevClosePrice):
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate*100:+.2f}%")
        self.label_4.setText(f"{volume:.4f} {self.ticker}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value / 100000000:,.1f} 억")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_12.setText(f"{bidVolume/askVolume:.2f}%")
        self.label_14.setText(f"{prevClosePrice:,}")

        self.__updateStyle()

    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue;")
            self.label_2.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_1.setStyleSheet("color:red;")
            self.label_2.setStyleSheet("background-color:red;color:white")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ow = OverviewWidget()
    ow.show()
    exit(app.exec_())
