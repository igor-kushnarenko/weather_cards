from peewee import *

user = 'postgres'
db_name = 'weather_cards'

db = PostgresqlDatabase(db_name, user=user, host='localhost')


class BaseModel(Model):
    class Meta:
        database = db


class Weather(BaseModel):
    id = PrimaryKeyField(null=False)
    date = DateTimeField(unique=True)
    weekday = CharField(max_length=20)
    temp_max = CharField(max_length=10)
    temp_min = CharField(max_length=10)
    clouds = CharField(max_length=50)

    class Meta:
        db_table = "weather_cards"
        order_by = ('date',)
