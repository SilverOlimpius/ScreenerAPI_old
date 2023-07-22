import yfinance as yf
import pandas as pd

def get_currency_data(currency_symbol, start_date, end_date):
    currency_data = yf.download(currency_symbol, start=start_date, end=end_date)
    return currency_data

# Задаем даты начала и конца периода
start_date = "2013-01-01"
end_date = "2023-07-18"

# Получаем данные для курса китайского юаня (CNY) к доллару США (USD)
currency_symbol = "USDRUB=X"
currency_data = get_currency_data(currency_symbol, start_date, end_date)

# Вычисляем изменение курса
initial_rate = currency_data["Close"].iloc[0]
final_rate = currency_data["Close"].iloc[-1]
rate_change = ((final_rate / initial_rate)**1/10)*100

# Выводим результат
print("Начальный курс:", initial_rate)
print("Конечный курс:", final_rate)
print("Изменение курса во сколько раз:", rate_change)
