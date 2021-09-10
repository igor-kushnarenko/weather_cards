import peewee
from models import db, Weather

if __name__ == '__main__':
    try:
        db.connect()
        Weather.create_table()
    except peewee.InternalError as px:
        print(str(px))
