import os

import cv2
from PIL import Image


class ImageMaker:
    """Класс принимает запись из БД и формирует изображение карточки с прогнозом погоды."""
    card_template_path = 'static/external_data/probe.jpg'
    sun_template_path = 'static/external_data/weather_img/sun.jpg'
    cloud_template_path = 'static/external_data/weather_img/cloud.jpg'
    snow_template_path = 'static/external_data/weather_img/snow.jpg'
    rain_template_path = 'static/external_data/weather_img/rain.jpg'

    def __init__(self, db_row):
        self.db_row = db_row

    def draw_card(self):
        card_img = cv2.imread(self.card_template_path, cv2.IMREAD_COLOR)

        font_scale = .9
        thickness = 1
        coord_table = ((120, 35), (50, 190), (270, 190), (50, 240), (120, 70))
        colors_dict = {'yellow': (0, 255, 255), 'grey': (73, 73, 73), 'dark_blue': (86, 57, 48), 'blue': (86, 57, 48)}

        date_datetime = self.db_row.date
        date_str = date_datetime.strftime("%d-%m-%Y")
        weekday = self.db_row.weekday
        temp_max = self.db_row.temp_max
        temp_min = self.db_row.temp_min
        clouds = self.db_row.clouds
        print(clouds)

        color = str
        logo = str

        if 'Ясно' in clouds:
            sun_img = cv2.imread(self.sun_template_path, cv2.IMREAD_COLOR)
            color = colors_dict['yellow']
            logo = sun_img
        elif 'облачность' or 'Облачно' in clouds:
            cloud_img = cv2.imread(self.cloud_template_path, cv2.IMREAD_COLOR)
            color = colors_dict['grey']
            logo = cloud_img
        elif 'Снег' or 'снег' in clouds:
            snow_img = cv2.imread(self.snow_template_path, cv2.IMREAD_COLOR)
            color = colors_dict['blue']
            logo = snow_img
        elif 'Дождь' or 'дождь' in clouds:
            rain_img = cv2.imread(self.rain_template_path, cv2.IMREAD_COLOR)
            color = colors_dict['dark_blue']
            logo = rain_img

        self.draw_gradient(color, card_img)
        self.paste_logo(card_img, logo)

        cv2.putText(card_img, f'Прогноз на {date_str}', coord_table[0], cv2.FONT_HERSHEY_COMPLEX, font_scale, thickness)
        cv2.putText(card_img, weekday, coord_table[4], cv2.FONT_HERSHEY_COMPLEX, font_scale, thickness)
        cv2.putText(card_img, f'День: {temp_max}', coord_table[1], cv2.FONT_HERSHEY_COMPLEX, font_scale, thickness)
        cv2.putText(card_img, f'Ночь: {temp_min}', coord_table[2], cv2.FONT_HERSHEY_COMPLEX, font_scale, thickness)
        cv2.putText(card_img, f'{clouds}', coord_table[3], cv2.FONT_HERSHEY_COMPLEX, font_scale, thickness)

        self.save_ready_card(card_img, date_str)

    def save_ready_card(self, card_img, date_str):
        if not os.path.exists('cards/'):
            os.mkdir('cards/')
        save_path = f'cards/{date_str}.jpg'
        cv2.imwrite(filename=save_path, img=card_img)
        img = Image.open(save_path)
        img.show()

    def paste_logo(self, card_img, logo_img):
        """Вставляет логотип погоды в изображение"""
        rows, cols, channels = logo_img.shape
        roi = card_img[0:rows, 0:cols]
        sun_img_gray = cv2.cvtColor(logo_img, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(sun_img_gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        card_img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
        sun_img_fg = cv2.bitwise_and(logo_img, logo_img, mask=mask)
        dst = cv2.add(card_img_bg, sun_img_fg)
        card_img[0:rows, 0:cols] = dst

    def draw_gradient(self, color, image):
        """Рисует градиент на изображении"""
        y_0, y_1, y_2 = (color[0], color[1], color[2])
        image_height = image.shape[0]
        image_width = image.shape[1]
        for _ in range(image_height):
            cv2.line(image, (0, image_height), (image_width, image_height), (y_0, y_1, y_2), 1)
            y_0 += 1.5
            y_1 += 1.5
            y_2 += 1.5
            image_height -= 1
