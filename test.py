import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mplfinance.original_flavor import candlestick2_ohlc
import matplotlib.ticker as ticker
import pyupbit

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.candle_stick()

    def setupUI(self):
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle("chart")

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def candle_stick(self):
        df = pyupbit.get_ohlcv("KRW-BTC", count=30)

        ax = self.fig.add_subplot(111)

        day_list = []
        name_list = []
        for i, day in enumerate(df.index):
            if day.dayofweek == 0:
                day_list.append(i)
                name_list.append(day.strftime('%Y-%m-%d') + '(Mon)')

        ax.xaxis.set_major_locator(ticker.FixedLocator(day_list))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(name_list))

        candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup='r', colordown='b')

        ax.grid()

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
