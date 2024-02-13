import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_limit_as_days_month():

    endTime = get_server_timestamp()
    startTime = get_start_timestamp_for_server(endTime)

    limit = delta_days(end_timestamp=endTime / 1000, start_timestamp=startTime / 1000) + 1

    return limit


def get_server_timestamp():

    base_endpoint = 'https://data-api.binance.vision'
    server_time_endpoint = base_endpoint + '/api/v3/time'
    server_time_responce = requests.get(server_time_endpoint)

    return server_time_responce.json()['serverTime']  # текущая временная метка прямо сейчас в UTC, тип int (мкс - последние три цифры)


def get_start_timestamp_for_server(end_timestamp_for_server):

    utc_timestamp = end_timestamp_for_server / 1000
    startTime_timestamp = month_ago_utc_timestamp(utc_timestamp)

    return int(startTime_timestamp * 1000)  # временная метка ровно месяц назад в UTC для сервера

def delta_days(start_timestamp, end_timestamp):

    end_datetime = datetime.utcfromtimestamp(end_timestamp)
    start_datetime = datetime.fromtimestamp(start_timestamp)

    return (end_datetime - start_datetime).days

def month_ago_utc_timestamp(utc_timestamp):

    dt = datetime.utcfromtimestamp(utc_timestamp)

    datetime_month_time_ago = dt - relativedelta(months=1)

    return datetime_month_time_ago.timestamp()




