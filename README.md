Weather forecast
====
* Script for the weather forecast.
* Output of the forecast to the console.
* Output of cards with a forecast.


Requirements
=====
* Python 3.x
* bs4
* fake-useragent
* lxml
* numpy
* opencv-python
* peewee
* Pillow
* psycopg2 (postgres driver)
* requests
* soupsieve


Download/Installation
====
* git clone https://github.com/igor-kushnarenko/weather_cards
* pip3 install -r requirements.txt --user

if pip3 is missing:
* apt-get install python3-setuptools
* easy_install3 pip
* pip3 install -r requirements.txt


Features
====
* Weather forecast for today, tomorrow, on the date, for the period.
* Checking the forecast on the command line.

Commands for console
====
Weather update
* python weather_console.py update

Weather for today
* python weather_console.py today

Weather for tomorrow
* python weather_console.py tomorrow

Weather for date
* python weather_console.py to_date

Weather for period
* python weather_console.py from_to