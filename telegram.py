import telepot
import pyupbit
import sys
import pandas as pd

def send(ticker):
    token = "1869660692:AAGDTzSc7E_5l8uJFV8Xu91_RuSCRRnAk1M"
    bot = telepot.Bot(token)
    price = pyupbit.get_current_price("KRW-"+ticker)
    message = ticker + " - " + str(price) + "원"
    bot.sendMessage(chat_id=1682338172, text=message)