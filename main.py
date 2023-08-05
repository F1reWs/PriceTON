import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import requests

api_token = "YOUR_CRYPTOCOMPARE_API_TOKEN"

API_URL = f"https://min-api.cryptocompare.com/data/price?fsym=USD&tsyms=TONCOIN&api_key={api_token}"

TOKEN = "YOUR_BOT_TOKEN"
CHANNEL_ID = "@YOUR_CHANNEL_USERNAME"

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def get_ton_rate() -> float:
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
             data = response.json()
             curs = round(data['TONCOIN'], 5)
             return curs
        else:
            raise Exception("Failed to get TON rate")
    except Exception as e:
        print(f"Error while getting TON rate: {str(e)}")

async def schedule_usdt_rate():
    new_rate = await get_ton_rate()

    while True:
        old_rate = new_rate
        new_rate = await get_ton_rate()

        if old_rate > new_rate:
            message = f"{new_rate} TON / 1 USD 🟢"
            await bot.send_message(chat_id=CHANNEL_ID, text=message)
        elif old_rate < new_rate:
            message = f"{new_rate} TON / 1 USD 🔴"
            await bot.send_message(chat_id=CHANNEL_ID, text=message)

        await asyncio.sleep(300)

async def on_startup(dp) -> None:
    await schedule_usdt_rate()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup(dp))
    loop.run_until_complete(dp.start_polling())
