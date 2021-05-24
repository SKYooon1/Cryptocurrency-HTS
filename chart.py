import sys
import time
import pyupbit
'''
import mpl_finance
import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as web
'''
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtChart import QLineSeries, QChart, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt, QDateTime, QThread, pyqtSignal


class PriceWorker(QThread):
    dataSent = pyqtSignal(float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            data = pyupbit.get_current_price(self.ticker)
            time.sleep(1)
            self.dataSent.emit(data)

    def close(self):
        self.alive = False


class ChartWidget(QWidget):
    def __init__(self, parent=None, ticker="KRW-BTC"):
        super().__init__(parent)
        uic.loadUi("chart.ui", self)
        self.ticker = ticker
        self.viewLimit = 128

        self.priceData = QLineSeries()
        self.priceChart = QChart()
        self.priceChart.addSeries(self.priceData)
        self.priceChart.legend().hide()
        ''' 캔들차트 띄우는 코드인데 창을 따로 띄우는거라 위젯에 넣는 법을 모르겠음
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(111)
        self.df = pyupbit.get_ohlcv("KRW-BTC")
        mpl_finance.candlestick2_ohlc(self.ax, self.df['open'], self.df['high'], self.df['low'], self.df['close'],
                                      width=0.5, colorup='r', colordown='b')'''
        axisX = QDateTimeAxis()
        axisX.setFormat("hh:mm:ss")
        axisX.setTickCount(4)
        dt = QDateTime.currentDateTime()
        axisX.setRange(dt, dt.addSecs(self.viewLimit))

        axisY = QValueAxis()
        axisY.setVisible(False)

        self.priceChart.addAxis(axisX, Qt.AlignBottom)
        self.priceChart.addAxis(axisY, Qt.AlignRight)
        self.priceData.attachAxis(axisX)
        self.priceData.attachAxis(axisY)
        self.priceChart.layout().setContentsMargins(0, 0, 0, 0)

        self.priceView.setChart(self.priceChart)
        self.priceView.setRenderHints(QPainter.Antialiasing)

        self.pw = PriceWorker(ticker)
        self.pw.dataSent.connect(self.appendData)
        self.pw.start()

    def appendData(self, currPrice):
        if len(self.priceData) == self.viewLimit:
            self.priceData.remove(0)
        dt = QDateTime.currentDateTime()
        self.priceData.append(dt.toMSecsSinceEpoch(), currPrice)
        self.__updateAxis()

    def __updateAxis(self):
        pvs = self.priceData.pointsVector()
        dtStart = QDateTime.fromMSecsSinceEpoch(int(pvs[0].x()))
        if len(self.priceData) == self.viewLimit:
            dtLast = QDateTime.fromMSecsSinceEpoch(int(pvs[-1].x()))
        else:
            dtLast = dtStart.addSecs(self.viewLimit)

        ax = self.priceChart.axisX()
        ax.setRange(dtStart, dtLast)

        ay = self.priceChart.axisY()
        dataY = [v.y() for v in pvs]
        ay.setRange(min(dataY), max(dataY))

    def closeEvent(self, event):
        self.pw.close()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    cw = ChartWidget()
    cw.show()
    exit(app.exec_())
