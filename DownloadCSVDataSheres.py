import certifi
import ssl
import json
import datetime
import time
import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

def just_take(Data, name_row):
    for item in Data:
        number = item[name_row]
    return number

def get_jsonparsed_data(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    return json.loads(data)

def extract_selected_data(data, fields):
    selected_data = []

    for item in data:
        selected_fields = {field: item[field] for field in fields}
        selected_data.append(selected_fields)

    return selected_data

allTicket = get_jsonparsed_data(("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=96530795198b481710ae7b955d34d876"))
start_time = datetime.datetime.now()
DATASHARES = []
STOCK_with_ERROR = []
list_share = ['IBP', 'MBUU', 'GTN','PATK','REGN','LGIH','AMN','WGO','LCII','CLFD','META','VCTR','WAL','MED','NVDA']

# уже скаченные данные:
folder_path = 'DataShares'  # Путь к папке DataShares, предполагая, что она находится в той же директории
file_names = []
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        share_name = filename.replace('.csv', '')
        file_names.append(share_name)
formatted_names = ', '.join(file_names)
formatted_names = f"[ {formatted_names} ]"

remaining_shares = [value for value in allTicket if value not in formatted_names]

#allTicket = list_share
for ShareTicket in allTicket:
    print(ShareTicket)
    limit = 'limit=150'
    key = '&apikey=96530795198b481710ae7b955d34d876'
    try:
        income_statement = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/income-statement/'+ShareTicket+'?'+limit+key)
        balance_sheet = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/balance-sheet-statement/'+ShareTicket+'?'+limit+key)
        price_statement = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/enterprise-values/'+ShareTicket+'?'+limit+key)
        metrics = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/key-metrics/'+ShareTicket+'?'+limit+key)
        IndustrialClass = get_jsonparsed_data('https://financialmodelingprep.com/api/v4/standard_industrial_classification?symbol=' + ShareTicket + key)

        income_fields = ["date", "symbol", "weightedAverageShsOutDil", "revenue", "operatingIncome", "netIncome", "eps", "reportedCurrency"]
        balance_fields = ["date", "symbol", "totalAssets", "totalEquity"]
        price_fields = ["date", "symbol", "stockPrice"]
        metrics_fields = ["date", "symbol", "revenuePerShare", "cashPerShare", "bookValuePerShare", "tangibleBookValuePerShare", "marketCap", "peRatio", "pbRatio", "ptbRatio", "debtToAssets"]
        try:
            Industrial = ((just_take(IndustrialClass, 'industryTitle')))
        except:
            Industrial = None

        income_selected_data = extract_selected_data(income_statement, income_fields)
        balance_selected_data = extract_selected_data(balance_sheet, balance_fields)
        price_selected_data = extract_selected_data(price_statement, price_fields)
        metrics_selected_data = extract_selected_data(metrics, metrics_fields)

        income_df = pd.DataFrame(income_selected_data)
        balance_df = pd.DataFrame(balance_selected_data)
        price_df = pd.DataFrame(price_selected_data)
        metrics_df = pd.DataFrame(metrics_selected_data)

        merged_df = pd.merge(income_df, balance_df, on=["date", "symbol"])
        merged_df = pd.merge(merged_df, price_df, on=["date", "symbol"], how="left")
        merged_df = pd.merge(merged_df, metrics_df, on=["date", "symbol"], how="left")
        merged_df['Industrial'] = Industrial

        print(merged_df)

        # Путь к папке "DataShares"
        output_folder = "DataShares"

        # Путь к файлу CSV
        csv_file_path = os.path.join(output_folder, ShareTicket + '.csv')

        # Сохранение DataFrame в CSV
        merged_df.to_csv(csv_file_path, index=False)

        DATASHARES.append([ShareTicket])
        complite = round(len(DATASHARES) / len(allTicket) * 100, 2)
        end_time = datetime.datetime.now()
        time_spend = end_time - start_time

        print('complicte', complite, '%')
        print("Время выполнения составляет: ", time_spend)
        total_seconds = int(time_spend.total_seconds())
        if complite > 0:
            remaining_time = (total_seconds/complite) * (100-complite)
        else:
            remaining_time = 0
        time_for_end = datetime.timedelta(seconds=remaining_time)

        print('оставшееся время:', time_for_end)

    except:
        print('ERROR: ',ShareTicket)
        STOCK_with_ERROR.append([ShareTicket])
print('All ERROR')
print(STOCK_with_ERROR)
