#!/usr/bin/env python
import certifi
import ssl
import json
import concurrent.futures
import pandas as pd
import datetime

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


def count_persent_grown(EnterData, name_row_for_count):
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
        grown_pet_year = grown ** (1 / length)
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


def count_tangROA(DataWithUP, nameUP, DataWithDOWN, nameDOWN, YearStartCount):
    DataUp = []
    try:
        for item in DataWithUP:
            row_for_count = item[nameUP]
            calendarYear = item['calendarYear']
            row = [calendarYear, row_for_count]
            DataUp.append(row)
        DataDown = []
        for item in DataWithDOWN:
            row_for_count = item[nameDOWN]
            calendarYear = item['calendarYear']
            allIntangibleAssets = item['goodwillAndIntangibleAssets']
            tangibleAssets = row_for_count - allIntangibleAssets
            row = [calendarYear, tangibleAssets]
            DataDown.append(row)
        DataPercentage = []
        for i in range(len(DataUp)):
            try:
                if int(DataUp[i][0]) >= int(YearStartCount):
                    if DataUp[i][0] == DataDown[i][0]:
                        percentage = DataUp[i][1] / (DataDown[i][1])
            except:
                percentage = 1
            DataPercentage.append(percentage)
        Mean = sum(DataPercentage) / len(DataPercentage)
    except:
        Mean = 0
    return Mean  # , DataPercentage


def exround(number, signs):
    try:
        result = round(number, signs)
    except:
        result = 0
    return result


def create_data_about_share(ShareTicket, limit):
    income_statement = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/income-statement/' + ShareTicket + '?' + limit + key)
    balance_sheet = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/balance-sheet-statement'+ ShareTicket + '?' + limit + key)
    #cash_flow = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/cash-flow-statement/'+ShareTicket+'?'+limit+key)
    # p/e peg
    ration = get_jsonparsed_data('https://financialmodelingprep.com/api/v3/ratios-ttm/'+ShareTicket+'?limit=1'+key)
    pe_ration = ((just_take(ration,'peRatioTTM')))

    row = [ShareTicket,exround(pe_ration, 2), exround(ShareBBfp, 2), exround(revenue_GPE, 2), exround(oIncome_GPE, 2),
            exround(eps_GPE, 2), exround(totalAssets_GPE, 2), exround(totalEquity_GPE, 2), exround(bvps_GPE, 2),
            exround(mean1ROA, 2), exround(mean5ROA, 2),currency,oldest_year]
    return row

def process_share(share):
    try:
        row = create_data_about_share(share, 'limit=10')
        return row
    except:
        return None

def process_all_shares(shares):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_share, shares)
    return [row for row in results if row is not None]

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    name_colomns = ['GrPetYear','pe','shr','rvn','opInm','eps','tAssts','tEqu','bvps','ROtA','5meanROtA','cur','old']

    allTicket = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=1a82bbd72952f10cfeb9bf5ba9b205b2")

    start_time = datetime.datetime.now()
    DATASHARES = process_all_shares(allTicket)
    df = pd.DataFrame(DATASHARES, columns=name_colomns)

    print(df)
    df.to_csv('DATASHARE.csv', index=False)
