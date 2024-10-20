import asyncio
from string import punctuation

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message

from app.filters import filterForChats

ban_words = {'сука', 'хуй', 'пидр', 'хуесос'}

group_router = Router()
group_router.message.filter(filterForChats(['group']))

@group_router.message(Command('admin'))
async def get_admins(message: Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    admins_list = [
        member.user.id 
        for member in admins_list 
        if member.status == 'creator' or member.status == 'administrator'
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@group_router.message()
@group_router.edited_message()
async def cmd_check(message: Message): 
    if ban_words.intersection(clean_text(message.text.lower()).split()):
        await message.delete()
        await message.answer(f"Нахуй с поля, {message.from_user.first_name}!")

