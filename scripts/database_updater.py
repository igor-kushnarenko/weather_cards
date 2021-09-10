from scripts.models import Weather


class DatabaseUpdater:
    def write_to_base(self, data):
        """Функция сохраняет данные в БД и обновляет уже существующие записи."""
        for forecast in data:
            date = forecast['date'],
            temp_max = forecast['temperature']['max'],
            temp_min = forecast['temperature']['min'],
            clouds = forecast['clouds'],
            weekday = forecast['weekday']

            rowid = (Weather
                     .insert(date=date[0],
                             temp_max=temp_max[0],
                             temp_min=temp_min[0],
                             clouds=clouds[0],
                             weekday=weekday)
                     .on_conflict(
                conflict_target=[Weather.date],
                preserve=[Weather.temp_max, Weather.temp_min, Weather.clouds, Weather.weekday],
                update={})
                     .execute())

    def read_db(self, date_from, date_to):
        """Возвращает объект базы"""
        return Weather.select().where(Weather.date.between(date_from, date_to))

    def clear_all_rows(self):
        """Удаляет все записи в БД"""
        delete_row = Weather.delete()
        delete_row.execute()
