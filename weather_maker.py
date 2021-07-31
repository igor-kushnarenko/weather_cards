import datetime
import locale

import requests
from bs4 import BeautifulSoup as bs4
from fake_useragent import UserAgent


USER_AGENT = UserAgent()
URL = 'https://sinoptik.com.ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-' \
      '%D0%BA%D1%80%D0%B0%D1%81%D0%BD%D0%BE%D0%B4%D0%B0%D1%80/10-%D0%B4%D0%BD%D0%B5%D0%B9'
NOW = datetime.datetime.now()

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
archive_data = {}


class WeatherMaker:
    def __init__(self):
        self.data = []

    def weather_parser(self):
        """Парсит данные погоды за следующие 10 дней и сохраняет в словарь"""
        response = requests.get(URL, USER_AGENT.ie)
        if response.status_code == 200:
            soup = bs4(response.text, 'lxml')
            items = soup.findAll(class_='weather__content_tab')
            for item in items:
                day = item.find(class_="weather__content_tab-date day_red").get_text(strip=True)
                month = item.find(class_="weather__content_tab-month").get_text(strip=True)
                weekday = item.find(class_="weather__content_tab-day").get_text(strip=True)
                temp_max = item.find("div", {"class": "weather__content_tab-temperature"}).get_text(strip=True)[13:-1]
                temp_min = item.find("div", {"class": "weather__content_tab-temperature"}).get_text(strip=True)[4:7]
                clouds = item.find(class_="show-tooltip").get_text(strip=True)

                date_str = f'{day} {month} {NOW.year}'
                date_datetime = datetime.datetime.strptime(date_str, '%d %B %Y')

                self.data.append(
                    {
                        'date': date_datetime.date(),
                        'temperature': {'max': temp_max, 'min': temp_min},
                        'clouds': clouds,
                        'weekday': weekday,
                    }
                )
        return self.data
