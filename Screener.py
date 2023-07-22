import yfinance as yf
import pandas as pd

def get_currency_data(currency_symbol, start_date, end_date):
    currency_data = yf.download(currency_symbol, start=start_date, end=end_date)
    return currency_data

# Задаем даты начала и конца периода
start_date = "2013-01-01"
end_date = "2023-07-18"

def cer_rate_change(ticket_cer):
    currency_symbol = 'USD'+ticket_cer+'=X'
    currency_data = get_currency_data(currency_symbol, start_date, end_date)

    # Вычисляем изменение курса
    initial_rate = currency_data["Close"].iloc[0]
    final_rate = currency_data["Close"].iloc[-1]
    rate_change = ((final_rate / initial_rate)**1/10)*100
    print(rate_change, ' ',ticket_cer)

    return rate_change


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DATASHARE = pd.read_csv('merged_df.csv')

filter1 = DATASHARE['pe'] <= 25
filter2 = DATASHARE['shr'] <= 10
filter3 = DATASHARE['revenue'] >= 20
filter4 = DATASHARE['opInm'] >= 15
filter5 = DATASHARE['eps'] >= 15
filter6 = DATASHARE['Assets'] >= 15
filter7 = DATASHARE['Equity'] >= 15
filter8 = DATASHARE['bvps'] >= 15
filter9 = DATASHARE['ROtA'] >= 10
filter10 = DATASHARE['5ROtA'] >= 10
filter11 = DATASHARE['10ROtA'] >= 10
filter12 = DATASHARE['bad5y'] <= 1
filter13 = DATASHARE['bad10y'] <= 2
filter14 = DATASHARE['old'] == 2013
filter15 = DATASHARE['cur'] != 'яCNY'

screener = DATASHARE[(filter1) & (filter2) & (filter3) & (filter4) & (filter5) & (filter6) & (filter7) & (filter8) & (filter9) & (filter10) & (filter11) & (filter12)& (filter13)& (filter14)& (filter15)]
sorted_data = screener.sort_values(by='bvps', ascending=False)
sorted_data = sorted_data.reset_index(drop=True)

data_CerChanges = []
for element in range(len(sorted_data)):
    if sorted_data.loc[element, 'cur'] != 'USD':
        CerChanges = cer_rate_change(sorted_data.loc[element,'cur'])
    if sorted_data.loc[element, 'cur'] == 'USD':
        CerChanges = 0
    data_CerChanges.append(CerChanges)

print(len(sorted_data))
sorted_data["CerChanges"] = data_CerChanges
sorted_data['revenue'] = sorted_data['revenue'] - sorted_data['CerChanges']
sorted_data['opInm'] = sorted_data['opInm'] - sorted_data['CerChanges']
sorted_data['eps'] = sorted_data['eps'] - sorted_data['CerChanges']
sorted_data['Assets'] = sorted_data['Assets'] - sorted_data['CerChanges']
sorted_data['Equity'] = sorted_data['Equity'] - sorted_data['CerChanges']
sorted_data['bvps'] = sorted_data['bvps'] - sorted_data['CerChanges']

filter3 = sorted_data['revenue'] >= 20
filter4 = sorted_data['opInm'] >= 15
filter5 = sorted_data['eps'] >= 15
filter6 = sorted_data['Assets'] >= 15
filter7 = sorted_data['Equity'] >= 15
filter8 = sorted_data['bvps'] >= 15

final_data = sorted_data[(filter3) & (filter4) & (filter5) & (filter6) & (filter7) & (filter8)]
final_data = final_data.sort_values(by='bvps', ascending=False)
print(final_data) # посчитать изминение к курсу доллара и отнять его от всех показателей рост
