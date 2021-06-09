import smtplib
from pyupbit import WebSocketManager
from email.mime.text import MIMEText 	#텍스트를 위해서

host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
port = "587"

def sendMail(ticker):
    global host, port

    senderAddr = "cryptocurrencyhts@gmail.com"  # 보내는 사람 email 주소.
    recipientAddr = "osjin6633@gmail.com"  # 받는 사람 email 주소.

    wm = WebSocketManager("ticker", ["KRW-" + f"{ticker}"])
    data = wm.get()
    text = ticker + "\n현재가 - " + str(data['trade_price']) + "원\n" + "고가 - " \
              + str(data['high_price']) + "원\n" + "저가 - " + str(data['low_price']) + "원"
    msg = MIMEText(text)
    msg['Subject'] = "information of Coin you've chose"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("cryptocurrencyhts@gmail.com", "cryptohts1!")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()
