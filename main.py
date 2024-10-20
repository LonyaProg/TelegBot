import asyncio
import os
from logging import basicConfig, getLogger, INFO

from dotenv import find_dotenv, load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.handlers.private_handlers import private_router
from app.handlers.group_handlers import group_router
from app.handlers.admin_private import admin_router
from command import private

load_dotenv(find_dotenv())

bot = Bot(token = os.getenv('TOKEN'), default = DefaultBotProperties(parse_mode = ParseMode.HTML))
dp = Dispatcher()
bot.my_admins_list = []
basicConfig(level = INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging = getLogger(__name__)

dp.include_router(private_router)
dp.include_router(admin_router)
dp.include_router(group_router)

async def main():
    await bot.delete_webhook(drop_pending_updates = True)
    await bot.set_my_commands(commands = private, scope = BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')