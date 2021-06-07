import mimetypes
import smtplib
import pyupbit
from email.mime.base import MIMEBase 	#파일첨부 위해서
from email.mime.text import MIMEText 	#텍스트를 위해서
from email.mime.image import MIMEImage 	#이미지를 위해서

host = "smtp.gmail.com"  # Gmail STMP 서버 주소.
port = "587"

def sendMail(ticker):
    global host, port

    senderAddr = "cryptocurrencyhts@gmail.com"  # 보내는 사람 email 주소.
    recipientAddr = "osjin6633@gmail.com"  # 받는 사람 email 주소.

    text = ticker + " " + str(pyupbit.get_current_price("KRW-"+ticker))
    msg = MIMEText(text)
    msg['Subject'] = "Current Price of ticker you've chose"
    msg['From'] = senderAddr
    msg['To'] = recipientAddr

    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login("cryptocurrencyhts@gmail.com", "cryptohts1!")
    s.sendmail(senderAddr, [recipientAddr], msg.as_string())
    s.close()
