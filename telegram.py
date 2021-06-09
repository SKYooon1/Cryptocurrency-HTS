import telepot
from pyupbit import WebSocketManager

def send(ticker):
    token = "1869660692:AAGDTzSc7E_5l8uJFV8Xu91_RuSCRRnAk1M"
    bot = telepot.Bot(token)
    wm = WebSocketManager("ticker", ["KRW-"+f"{ticker}"])
    data = wm.get()
    message = ticker + "\n현재가 - " + str(data['trade_price']) + "원\n" + "고가 - "\
              + str(data['high_price']) + "원\n" + "저가 - " + str(data['low_price']) + "원"

    bot.sendMessage(chat_id=1682338172, text=message)