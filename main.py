import sys
import pyupbit
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
form_class = uic.loadUiType("main.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button.clicked.connect(self.clickBtn)

    def clickBtn(self):
        if self.button.text() == "매매시작":
            apiKey = self.apiKey.text()
            secKey = self.secKey.text()
            if len(apiKey) != 32 or len(secKey) != 32:
                self.textEdit.append("KEY가 올바르지 않습니다.")
                return
            else:
                self.b = pyupbit.Upbit(apiKey, secKey)
                balance = self.b.get_balance(self.ticker)
                if balance == None:
                    self.textEdit.append("KEY가 올바르지 않습니다.")
                    return
            self.button.setText("매매중지")
            self.textEdit.append("------ START ------")
            self.textEdit.append(f"보유 현금 : {self.balance[2]} 원")

        else:
            self.textEdit.append("------- END -------")
            self.button.setText("매매시작")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    exit(app.exec_())