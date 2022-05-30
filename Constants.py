import requests
import json


def get_public_holidays():
    public_holidays = []
    response = requests.get(
        f"https://holidayapi.com/v1/holidays?pretty&key=de018c99-482f-41a5-9520-dd3cbe8eecc8&country=IN&year=2021")
    dict_response = response.json()
    dict_holidays = dict_response['holidays']
    for holiday in dict_holidays:
        holiday_date = holiday['date']
        public_holidays.append(holiday_date)
    return public_holidays
