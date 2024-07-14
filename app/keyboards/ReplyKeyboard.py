from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Текущая погода")],
                                     [KeyboardButton(text="Прогноз погоды на 7 дней")]],
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт меню...')

current = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выбрать город")],
                                        [KeyboardButton(text="По моему местоположению")]],
                              resize_keyboard=True,
                              input_field_placeholder='Выберите пункт меню...')

location = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Дать разрешение на местоположени", request_location=True)]],
                               resize_keyboard=True)