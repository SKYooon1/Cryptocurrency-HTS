import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mplfinance.original_flavor import candlestick2_ohlc
import pyupbit
import pandas
import time

CHTICKER = "BTC"

class ChartWorker(QThread):
    dataSent = pyqtSignal(pandas.core.frame.DataFrame)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.running = True

    def run(self):
        while self.running:
            data = pyupbit.get_ohlcv("KRW-"+CHTICKER, interval='minute30', count=30)
            self.dataSent.emit(data)
            time.sleep(1)

    def close(self):
        self.running = False

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-"+CHTICKER):
        super().__init__(parent)
        self.setupUI()
        self.ticker = ticker

        self.ow = ChartWorker("KRW-"+CHTICKER)
        self.ow.dataSent.connect(self.candle_stick)
        self.ow.start()

    def setupUI(self):
        self.setWindowTitle("chart")

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

    def candle_stick(self, data):
        self.ax = self.fig.add_subplot(111)

        self.ax.set_xticks([])

        candlestick2_ohlc(self.ax, data['open'], data['high'], data['low'], data['close'],
                          width=0.5, colorup='r', colordown='b')

        self.ax.grid()

        self.canvas.draw()
        self.fig.clear()

    def closeEvent(self, event):
        self.ow.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartWidget()
    window.show()
    app.exec_()
