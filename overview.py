import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from pyupbit import WebSocketManager, get_current_price
from PyQt5.QtCore import QThread, pyqtSignal
import time
from currency_converter import CurrencyConverter
import ccxt
import spam

OVTICKER = "BTC"
GP = False

class OverViewWorker(QThread):
    dataSent = pyqtSignal(str, int, float, float, int, float, int, float, float, int, float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.running = True
        self.exrate = self.getExRate()

    def getExRate(self):
        c = CurrencyConverter('http://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip')
        exrate = (c.convert(1, "KRW", "USD"))
        return exrate

    def run(self):
        global OVTICKER
        binance = ccxt.binance()
        markets = binance.fetch_tickers()
        while self.running:
            global GP
            wm = WebSocketManager("ticker", ["KRW-"+f"{OVTICKER}"])
            kticker = get_current_price("KRW-" + OVTICKER) * self.exrate
            if (OVTICKER + '/USDT') in markets:
                bticker = binance.fetch_ticker(OVTICKER + '/USDT')['close']
                gp = spam.kimch_primium(kticker, bticker)
                GP = True
            else:
                gp = 0
                GP = False
            data = wm.get()
            wm.terminate()
            self.dataSent.emit(str  (OVTICKER),
                               int  (data['trade_price']),
                               float(data['signed_change_rate']),
                               float(data['acc_trade_volume_24h']),
                               int  (data['high_price']),
                               float(data['acc_trade_price_24h']),
                               int  (data['low_price']),
                               float(data['acc_ask_volume']),
                               float(data['acc_bid_volume']),
                               int  (data['prev_closing_price']),
                               float(gp))
            time.sleep(1.0)

    def close(self):
        self.running = False

class OverviewWidget(QWidget):
    def __init__(self, parent=None, ticker=OVTICKER):
        super().__init__(parent)
        uic.loadUi("overview.ui", self)
        self.ticker = ticker
        self.ow = OverViewWorker("KRW-"+ticker)
        self.ow.dataSent.connect(self.fillData)
        self.ow.start()

    def fillData(self, OVTICKER, currPrice, chgRate, volume, highPrice, value,
                 lowPrice, askVolume, bidVolume, prevClosePrice, GimchiPremium):
        self.label.setText(f"{OVTICKER}")
        self.label_1.setText(f"{currPrice:,}")
        self.label_2.setText(f"{chgRate*100:+.2f}%")
        self.label_4.setText(f"{volume:.4f} {OVTICKER}")
        self.label_6.setText(f"{highPrice:,}")
        self.label_8.setText(f"{value / 100000000:,.1f} ???")
        self.label_10.setText(f"{lowPrice:,}")
        self.label_12.setText(f"{bidVolume/askVolume*100:.2f}%")
        self.label_14.setText(f"{prevClosePrice:,}")
        global GP
        if GP:
            self.gimp.setText("?????? ???????????? " + f"{GimchiPremium:.2f}%")
        else:
            self.gimp.setText("?????? ???????????? ????????????")

        self.__updateStyle()

    def __updateStyle(self):
        if '-' in self.label_2.text():
            self.label_1.setStyleSheet("color:blue;")
            self.label_2.setStyleSheet("background-color:blue;color:white")
        else:
            self.label_1.setStyleSheet("color:red;")
            self.label_2.setStyleSheet("background-color:red;color:white")

    def closeEvent(self, event):
        self.ow.close()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ow = OverviewWidget()
    ow.show()
    exit(app.exec_())
