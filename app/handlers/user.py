from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command, StateFilter

import app.keyboards.ReplyKeyboard as kb
import app.requests as re

user_router = Router()

class current_weather(StatesGroup):
    choice = State()
    city = State()
    location = State()
    
class forecast(StatesGroup):
    choice = State()
    city = State()
    location = State()


@user_router.message(CommandStart())
async def start(message:Message):
    await message.answer("Бот о фактической погоде и прогнозах от Гидрометцентра", reply_markup=kb.main)
    
@user_router.message(F.text == "Текущая погода")
async def current_current_weather(message: Message, state : FSMContext):
    await message.answer("Выберите пункт меню", reply_markup=kb.current)
    await state.set_state(current_weather.choice)

@user_router.message(F.text == "Прогноз погоды на 7 дней")
async def current_forecast(message: Message, state : FSMContext):
    await message.answer("Выберите пункт меню", reply_markup=kb.current)
    await state.set_state(forecast.choice)
    
@user_router.message(current_weather.choice, F.text == "Выбрать город")
async def city_current_weather(message: Message, state : FSMContext):
    await message.answer("Введите название города", reply_markup=ReplyKeyboardRemove())
    await state.set_state(current_weather.city)

@user_router.message(forecast.choice, F.text == "Выбрать город")
async def city_forecast(message: Message, state : FSMContext):
    await message.answer("Введите название города", reply_markup=ReplyKeyboardRemove())
    await state.set_state(forecast.city)
    
@user_router.message(current_weather.city, F.text)
async def find_current_weather(message: Message, state : FSMContext):
    data = await re.find_current_requests(message.text)
    if data:
        await message.answer(f"погода в городе: {message.text}\nтемпература: {data['temp_c']}\nвлажность: {data['humidity']}\nскорость ветра: {data['wind_mph']}\nна улице: {data['text']}",
                              reply_markup=kb.main)
        await state.clear()
    else:
        await message.answer("Введины не допустимые данные")

@user_router.message(forecast.city, F.text)
async def find_forecast(message: Message, state : FSMContext):
    data = await re.find_forecast_requests(message.text)
    if data:
        for i in range(7):
            await message.answer(
                f"дата: {data['date'][i]}\nпогода в городе: {message.text}\nтемпература: {data['avgtemp_c'][i]}\nвлажность: {data['avghumidity'][i]}\
                \nна улице: {data['text'][i]}\nвосход солнца: {data['sunrise'][i]}\nзакат: {data['sunset'][i]}",
                 reply_markup=kb.main
                )
        await state.clear()
    else:
        await message.answer("Введины не допустимые данные")

@user_router.message(current_weather.choice, F.text == "По моему местоположению")
async def location_current_weather(message: Message, state : FSMContext):
    await message.answer("Дайте разрешение на прочтение вашего местоположения", reply_markup=kb.location)
    await state.set_state(current_weather.location)

@user_router.message(forecast.choice, F.text == "По моему местоположению")
async def location_forecast(message: Message, state : FSMContext):
    await message.answer("Дайте разрешение на прочтение вашего местоположения",  reply_markup=kb.location)
    await state.set_state(forecast.location)
    
@user_router.message(current_weather.location, F.location)
async def find_current_weather(message: Message, state : FSMContext):
    await message.delete()
    data = await re.find_current_location(message.location.latitude, message.location.longitude)
    if data:
        await message.answer(f"погода в городе: {data['name']}\nтемпература: {data['temp_c']}\nвлажность: {data['humidity']}\nскорость ветра: {data['wind_mph']}\nна улице: {data['text']}",
                             reply_markup=kb.main)
        await state.clear()
    else:
        await message.answer("Введины не допустимые данные")

@user_router.message(forecast.location, F.location)
async def find_forecast(message: Message, state : FSMContext):
    await message.delete()
    data = await re.find_forecast_location(message.location.latitude, message.location.longitude)
    if data:
        for i in range(7):
            await message.answer(
                f"дата: {data['date'][i]}\nпогода в городе: {data['name']}\nтемпература: {data['avgtemp_c'][i]}\nвлажность: {data['avghumidity'][i]}\
                \nна улице: {data['text'][i]}\nвосход солнца: {data['sunrise'][i]}\nзакат: {data['sunset'][i]}",
                 reply_markup=kb.main
                )
        await state.clear()
    else:
        await message.answer("Введины не допустимые данные")

@user_router.message(StateFilter('*'))
async def find(message: Message, state : FSMContext):
    await message.answer("Введины не допустимые данные1")



