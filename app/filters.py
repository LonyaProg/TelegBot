from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram import Bot


class filterForChats(Filter):
    def __init__(self, chats_list):
        self.chats_list = chats_list
    
    async def __call__(self, message: Message):
        return message.chat.type in self.chats_list
    
class IsAdmin(Filter):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, message: Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_admins_list