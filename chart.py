import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mplfinance.original_flavor import candlestick2_ohlc
import matplotlib.ticker as ticker
import pyupbit
import pandas
import time

class ChartWorker(QThread):
    dataSent = pyqtSignal(pandas.core.frame.DataFrame)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.running = True

    def run(self):
        while self.running:
            data = pyupbit.get_ohlcv(self.ticker, interval='minute30', count=30)
            self.dataSent.emit(data)
            time.sleep(0.4)

    def close(self):
        self.running = False

class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-BTC"):
        super().__init__(parent)
        self.setupUI()
        self.ticker = ticker

        self.ow = ChartWorker(self.ticker)
        self.ow.dataSent.connect(self.candle_stick)
        self.ow.start()

    def setupUI(self):
        self.setGeometry(600, 200, 700, 600)
        self.setWindowTitle("chart")

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def candle_stick(self, data):
        ax = self.fig.add_subplot(111)

        candlestick2_ohlc(ax, data['open'], data['high'], data['low'], data['close'],
                          width=0.5, colorup='r', colordown='b')

        self.canvas.draw()

    def closeEvent(self, event):
        self.ow.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChartWidget()
    window.show()
    app.exec_()
