import datetime

from database_updater import DatabaseUpdater
from image_maker import ImageMaker
from weather_maker import WeatherMaker
from models import Weather


class Manager:
    def print_forecast_to_console(self, db_row):
        """Вывод прогноза погоды в консоль."""
        date_datetime = db_row.date
        date_str = date_datetime.strftime("%d-%m-%Y")
        weekday = db_row.weekday
        temp_max = db_row.temp_max
        temp_min = db_row.temp_min
        clouds = db_row.clouds
        str_forecast = f'\nПрогноз на {date_str}, {weekday}\nДень: {temp_max}, Ночь: {temp_min}, Осадки: {clouds}'
        print(str_forecast)

    def parse_data_send_to_db(self):
        """Функция отправляет спарсенные данные в БД"""
        data = WeatherMaker().weather_parser()
        DatabaseUpdater().write_to_base(data)
        print('Погода обновлена.')

    def today_forecast(self):
        """Возвращает объект из БД за сегодняшнее число."""
        today = datetime.date.today()
        for db_row in Weather.select():
            day = db_row.date
            if day.date() == today:
                ImageMaker(db_row).draw_card()
                self.print_forecast_to_console(db_row)

    def tomorrow_forecast(self):
        """Возвращает объект за завтрашнее число из базы"""
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        for db_row in Weather.select():
            day = db_row.date
            if day.date() == tomorrow:
                ImageMaker(db_row).draw_card()
                self.print_forecast_to_console(db_row)

    def get_card_from_date(self):
        """Создание открытки за определенную дату"""
        month = int(input('Месяц: '))
        day = int(input('Дата: '))
        date_for_card = datetime.date(year=2021, month=month, day=day)
        for db_row in Weather.select():
            day = db_row.date.strftime("%Y-%m-%d")
            if day == str(date_for_card):
                ImageMaker(db_row).draw_card()
                self.print_forecast_to_console(db_row)

    def input_dates(self):
        while True:
            month = input('Месяц(напр.: 12): ')
            day_0 = input('Дата начала периода: ')
            day_1 = input('Дата окончания периода: ')
            if month.isdigit() and day_1.isdigit() and day_1.isdigit():
                try:
                    date_start = datetime.date(year=2021, month=int(month), day=int(day_0))
                    date_end = datetime.date(year=2021, month=int(month), day=int(day_1) + 1)
                except:
                    print(f'Введены некорректные данные. Повторите ввод.')
                    continue
                delta_1_day = datetime.timedelta(days=1)
                return date_start, date_end, delta_1_day
            else:
                print('Введите числовые значения!')
                continue

    def choice_dates_forecast(self):
        """Принимает даты, возвращает объект БД за эти даты"""
        get_dates = self.input_dates()
        database_reader = DatabaseUpdater()
        date_start = get_dates[0]
        date_end = get_dates[1]
        delta_1_day = get_dates[2]
        while date_start != date_end:
            for db_row in database_reader.read_db(date_start, date_end):
                day = db_row.date.strftime("%Y-%m-%d")
                if day == str(date_start):
                    ImageMaker(db_row).draw_card()
                    self.print_forecast_to_console(db_row)
            date_start = date_start + delta_1_day


def run():
    manager = Manager()
    print('Выберите прогноз: 1.На сегодня 2.На завтра 3.На дату 4.На период')
    user_input = int(input('Выбор: '))
    if user_input == 1:
        manager.today_forecast()
    elif user_input == 2:
        manager.tomorrow_forecast()
    elif user_input == 3:
        manager.get_card_from_date()
    elif user_input == 4:
        manager.choice_dates_forecast()


if __name__ == '__main__':
    run()
