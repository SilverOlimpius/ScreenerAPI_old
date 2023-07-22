#!/usr/bin/env python
import certifi
import ssl
import json
import datetime
import time
import pandas as pd
#import re

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    return json.loads(data)


def count_persent_grown(EnterData,name_row_for_count):
    Data = []
    try:
        for item in EnterData:
            row_for_count = item[name_row_for_count]
            calendarYear = item['calendarYear']
            row = [calendarYear, row_for_count]
            Data.append(row)
        newest = Data[0][1]
        length = len(Data) - 1
        oldest = Data[length][1]
        grown = newest / oldest
        grown_pet_year = grown ** (1/length)
    except:
        grown_pet_year = 0
    return grown_pet_year

def just_take(Data, name_row):
    for item in Data:
        number = item[name_row]
    return number

def just_take_old(Data, name_row):
    new_data = []
    for item in Data:
        calendarYear = item[name_row]
        row = [calendarYear]
        new_data.append(row)
    length = len(new_data) - 1
    oldest = new_data[length][0]
    return oldest

def count_tangROA(DataWithUP, nameUP, DataWithDOWN, nameDOWN,YearStartCount):
    DataUp = []
    try:
        for item in DataWithUP:
            row_for_count = item[nameUP]
            calendarYear = item['calendarYear']
            row = [calendarYear, row_for_count]
            if int(calendarYear) >= YearStartCount:
                DataUp.append(row)
        DataDown = []
        for item in DataWithDOWN:
            row_for_count = item[nameDOWN]
            calendarYear = item['calendarYear']
            allIntangibleAssets = item['goodwillAndIntangibleAssets']
            tangibleAssets = row_for_count - allIntangibleAssets
            row = [calendarYear, tangibleAssets]
            if int(calendarYear) >= YearStartCount:
                DataDown.append(row)
        DataPercentage = []
        for i in range(len(DataUp)):
            try:
                if int(DataUp[i][0]) >= int(YearStartCount):
                    if DataUp[i][0] == DataDown[i][0]:
                        percentage = DataUp[i][1]/(DataDown[i][1])
            except:
                percentage = 1
            DataPercentage.append(percentage)
        Mean = sum(DataPercentage) / len(DataPercentage)
        # Вычисляем значение, на которое среднее нужно уменьшить на 75%
        threshold = Mean*0.25
        # Подсчитываем количество чисел, меньших чем threshold
        count = sum(1 for num in DataPercentage if num < threshold)
    except:
        Mean = 0
        count = 0
    return Mean, count # , DataPercentage

def exround(number,signs):
    try:
        result = round(number, signs)
    except:
        result = 0
    return result


current_date = datetime.datetime.now()
ten_years_ago = current_date.year - 10
five_years_ago = current_date.year - 5
current_years = current_date.year - 1

key = '&apikey=1a82bbd72952f10cfeb9bf5ba9b205b2'
def create_data_abount_share(ShareTicket,limit):
    income_statement = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/income-statement/'+ShareTicket+'?'+limit+key)
    balance_sheet = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/balance-sheet-statement/'+ShareTicket+'?'+limit+key)
    #cash_flow = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/cash-flow-statement/'+ShareTicket+'?'+limit+key)
    #priсe_statement = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/historical-price-full/' + ShareTicket + key)
    IndustrialClass = get_jsonparsed_data('https://financialmodelingprep.com/api/v4/standard_industrial_classification?symbol=' + ShareTicket + key)
    # p/e peg
    ration = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/ratios-ttm/'+ShareTicket+'?limit=1'+key)
    pe_ration = ((just_take(ration,'peRatioTTM')))
    pb_ration = ((just_take(ration, 'priceToBookRatioTTM')))
    peg_ration = ((just_take(ration, 'pegRatioTTM')))
    Industrial = ((just_take(IndustrialClass, 'industryTitle')))

    #number = re.findall(r'\d+', limit)
    #limit_number = int(number[0])

    #for item in income_statement:
    #    print(json.dumps(item, indent=4))
    # for item in balance_sheet:
    #    print(json.dumps(item, indent=4))
    #for item in priсe_statement:
    #    print(json.dumps(item, indent=4))

    # revenue, operatingIncome, netIncome, eps, weightedAverageShsOutDil
    oldest_year = (just_take_old(income_statement, 'calendarYear'))
    ShareBB = ((count_persent_grown(income_statement,'weightedAverageShsOutDil')))
    ShareBBfp = ((count_persent_grown(income_statement,'weightedAverageShsOutDil')- 1)*100)
    revenue_GPE = ((count_persent_grown(income_statement,'revenue')- 1)*100)
    oIncome_GPE = ((count_persent_grown(income_statement,'operatingIncome')- 1)*100)
    nIncome_GPE = ((count_persent_grown(income_statement,'netIncome')- 1)*100)
    eps_GPE = ((count_persent_grown(income_statement,'eps')- 1)*100)

    # totalAssets, totalEquity,
    # сколько денег было потраченно на байбек всего, суммарные дивиденды. (потом посчитать сколько денег на байбек было потрачено на поощрения менеджерам)
    totalAssets_GPE = ((count_persent_grown(balance_sheet,'totalAssets')- 1)*100)
    totalEquity_GPE = ((count_persent_grown(balance_sheet,'totalEquity')- 1)*100)
    # для понимания на сколько рос баланс на акцию нужно рост балансовой стоимости поделить на ShareBB
    try:
        bvps_GPE = ((totalEquity_GPE / ShareBB))
    except:
        bvps_GPE = totalEquity_GPE

    mean10ROAnp, bad10y =count_tangROA(income_statement, 'netIncome', balance_sheet, 'totalAssets',ten_years_ago)
    mean5ROAnp, bad5y = count_tangROA(income_statement, 'netIncome', balance_sheet, 'totalAssets',five_years_ago)
    mean1ROAnp, bad1y = count_tangROA(income_statement, 'netIncome', balance_sheet, 'totalAssets',current_years)

    mean10ROA = mean10ROAnp *100
    mean5ROA = mean5ROAnp *100
    mean1ROA = mean1ROAnp *100

    currency = ((just_take(income_statement,'reportedCurrency')))

    row = [ShareTicket,exround(pe_ration, 2),exround(pb_ration, 2),exround(peg_ration, 2), exround(ShareBBfp, 2), exround(revenue_GPE, 2), exround(oIncome_GPE, 2),
            exround(eps_GPE, 2), exround(totalAssets_GPE, 2), exround(totalEquity_GPE, 2), exround(bvps_GPE, 2),
            exround(mean1ROA, 2), exround(mean5ROA, 2), exround(mean10ROA, 2),bad5y,bad10y,Industrial,currency,oldest_year]
    return row
#ShareTicket = 'LGIH'  # PHM DHI LGIH
#limit = 'limit=120'  # limit=120


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
name_colomns = ['GrPetYear','pe','pb','peg','shr','revenue','opInm','eps','Assets','Equity','bvps','ROtA','5ROtA','10ROtA','bad5y','bad10y','Industrial','cur','old'] #'10meanROA'

allTicket = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=1a82bbd72952f10cfeb9bf5ba9b205b2")
print(allTicket)


start_time = datetime.datetime.now()

DATASHARES = []
list_share = ['PHM', 'DHI', 'LGIH','AAPL','MSFT']

#allTicket = list_share
for share in allTicket:
    try:
        row = create_data_abount_share(share,'limit=10')
        DATASHARES.append(row)

        complite = exround(len(DATASHARES) / len(allTicket) * 100, 2)
        sellectDF = pd.DataFrame([row], columns=name_colomns)

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
        print(sellectDF)
    except:
        df = pd.DataFrame(DATASHARES, columns=name_colomns)
        df.to_csv('DATASHARE.csv', index=False)

df = pd.DataFrame(DATASHARES, columns=name_colomns)
# Установка опций отображения

# Вывод DataFrame
print(df)
df.to_csv('DATASHARE1.csv',index=False)

# а так же рост цены акций