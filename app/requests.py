import os
from pprint import pprint
from dotenv import find_dotenv, load_dotenv
from aiohttp import ClientSession
load_dotenv(find_dotenv())
async def find_current_requests(city: str, api_token = os.getenv('API_TOKEN')):
    try:
        async with ClientSession() as session:
            async with session.get(f"https://api.weatherapi.com/v1/current.json?key={api_token}&q={city}&lang=ru") as response:
                data = await response.json()
                req = {
                'temp_c':data['current']['temp_c'],
               'text':data['current']['condition']['text'],
               'humidity':data['current']['humidity'],
               'wind_mph':data['current']['wind_mph']}
                return req
    except Exception as ex:
        print(ex)
        return None
    
async def find_current_location(latitude: str, longitude: str, api_token = os.getenv('API_TOKEN')):
    try:
        async with ClientSession() as session:
            async with session.get(f"https://api.weatherapi.com/v1/current.json?key={api_token}&q={latitude},{longitude}&lang=ru") as response:
                data = await response.json()
                req = {
                'temp_c':data['current']['temp_c'],
               'text':data['current']['condition']['text'],
               'humidity':data['current']['humidity'],
               'wind_mph':data['current']['wind_mph'],
               'name':data['location']['name']}
                return req
    except Exception as ex:
        print(ex)
        return None
    
async def find_forecast_requests(city: str, api_token = os.getenv('API_TOKEN')):
    try:
        async with ClientSession() as session:
            async with session.get(f"https://api.weatherapi.com/v1/forecast.json?key={api_token}&q={city}&lang=ru&days=7") as response:
                data = await response.json()
                avgtemp_c, avghumidity, text, date, sunrise, sunset = [], [], [], [], [], []
                for i in data['forecast']['forecastday']:
                    date.append(i['date'])
                    avgtemp_c.append(i['day']['avgtemp_c'])
                    avghumidity.append(i['day']['avghumidity'])
                    text.append(i['day']['condition']['text'])
                    sunrise.append(i['astro']['sunrise'])
                    sunset.append(i['astro']['sunset'])
                return {'avgtemp_c':avgtemp_c, 'avghumidity':avghumidity, 'text':text, 'date':date, 'sunrise':sunrise, 'sunset':sunset}
    except Exception as ex:
        print(ex)
        return None
    
async def find_forecast_location(latitude: str, longitude: str, api_token = os.getenv('API_TOKEN')):
    try:
        async with ClientSession() as session:
            async with session.get(f"https://api.weatherapi.com/v1/forecast.json?key={api_token}&q={latitude},{longitude}&lang=ru&days=7") as response:
                data = await response.json()
                location = data['location']['name']
                avgtemp_c, avghumidity, text, date, sunrise, sunset = [], [], [], [], [], []
                for i in data['forecast']['forecastday']:
                    date.append(i['date'])
                    avgtemp_c.append(i['day']['avgtemp_c'])
                    avghumidity.append(i['day']['avghumidity'])
                    text.append(i['day']['condition']['text'])
                    sunrise.append(i['astro']['sunrise'])
                    sunset.append(i['astro']['sunset'])
                return {'avgtemp_c':avgtemp_c, 'avghumidity':avghumidity, 'text':text, 'date':date, 'name': location, 'sunrise':sunrise, 'sunset':sunset}
    except Exception as ex:
        print(ex)
        return None