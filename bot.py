import os
import requests
import asyncio
from aiogram import Bot, Dispatcher, types, Router, F

API_KEY = 'Ключ'

bot = Bot(token='Ключ')
dp = Dispatcher()

weather_router = Router()
dp.include_router(weather_router)


@weather_router.message(F.command == "start")
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города, чтобы узнать погоду.")

async def get_weather(message: types.Message):
    city = message.text
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']

        return f"Погода в {city}: {description}\nТемпература: {temp}°C\nВлажность: {humidity}%"
    else:
        return "Не удалось получить погоду. Пожалуйста, попробуйте еще раз."

@dp.message_handler()
async def handle_message(message: types.Message):
    weather_info = await get_weather(message.text)
    await message.reply(weather_info)

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())