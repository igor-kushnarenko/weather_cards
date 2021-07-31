import argparse

from weather import Manager

manager = Manager()

parser = argparse.ArgumentParser(
    prog='WeatherForecast',
    description='Weather forecast',
)
subparser = parser.add_subparsers()

"""Обновление базы"""
parser_weather_date = subparser.add_parser(
    'update',
    help='Обновление данных о погоде. '
         'При запросе происходит парсинг с сайта https://sinoptik.com.ru/. '
         'Пример ввода: python weather_console update')
parser_weather_date.set_defaults(func=manager.parse_data_send_to_db)

"""Погода за сегодняшнее число"""
parser_weather_date = subparser.add_parser(
    'today',
    help='Погода на сегодня. '
         'Пример ввода команды для запуска: python weather_console today')
parser_weather_date.set_defaults(func=manager.today_forecast)

"""Погода на завтра"""
parser_weather_date = subparser.add_parser(
    'tomorrow',
    help='Погода на завтра. '
         'Пример ввода команды для запуска: python weather_console tomorrow')
parser_weather_date.set_defaults(func=manager.tomorrow_forecast)

"""Погода на определенную дату"""
parser_weather_date = subparser.add_parser(
    'to_date',
    help='Погода на определенную дату. Что бы узнать погоду на 9 июля, '
         'необходимо ввести номер месяца: 7 и дату: 9. '
         'Пример ввода команды для запуска: python weather_console to_date')
parser_weather_date.set_defaults(func=manager.get_card_from_date)

"""Погода за период"""
parser_weather_date = subparser.add_parser(
    'from_to',
    help='Погода за период с _ по _. '
         'Пример ввода команды для запуска python weather_console from_to')
parser_weather_date.set_defaults(func=manager.choice_dates_forecast)

args = parser.parse_args()
args.func()

# в help стоит дообавлять больше информации, желательно с примерами ввода
# Добавьте в description аргументы, которые вы вводите для проверки работы программы