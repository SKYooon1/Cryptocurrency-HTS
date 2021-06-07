import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mplfinance.original_flavor import candlestick2_ohlc
import pyupbit

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.pushButtonClicked()

    def setupUI(self):
        self.setGeometry(600, 200, 1200, 600)
        self.setWindowTitle("PyChart Viewer v0.1")
        self.setWindowIcon(QIcon('icon.png'))

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        leftLayout = QHBoxLayout()
        leftLayout.addWidget(self.canvas)

        layout = QHBoxLayout()
        layout.addLayout(leftLayout)
        layout.setStretchFactor(leftLayout, 1)

        self.setLayout(layout)

    def pushButtonClicked(self):
        df = pyupbit.get_ohlcv("KRW-ETH", count=30)
        ax = self.fig.add_subplot(111)

        candlestick2_ohlc(ax, df['open'], df['high'], df['low'], df['close'], width=0.5, colorup='r', colordown='b')

        ax.grid()

        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()
