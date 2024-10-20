from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart, or_f
from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.utils.formatting import Bold, as_list, as_marked_section
import asyncio

from app.filters import filterForChats, IsAdmin
import app.keyboards.reply_keyboards as kb 

private_router = Router()
private_router.message.filter(filterForChats(['private']))

@private_router.message(F.photo)
async def photo_id(message: Message):
    id = message.photo[-1].file_id
    await message.answer(id)

@private_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text = 'Привет это виртуальный помошник!',
            reply_markup = kb.get_keyboard(
                'Меню',
                'О магазине',
                'Варианты оплаты',
                'Варианты оплаты',
                placeholder = 'Что вас интересует?',
                sizes = (2, 2)
            ),
        )
    
@private_router.message(or_f(Command('menu'), F.text.lower() == 'меню'))
async def cmd_menu(message: Message):
    await message.answer(text = 'Вот наше меню:', reply_markup = ReplyKeyboardRemove())

@private_router.message(or_f(Command('about'), F.text.lower() == 'о магазине'))
async def cmd_about(message: Message):
    await message.answer(text = 'О нас:')

@private_router.message(or_f(Command('payment'), F.text.lower() == 'варианты оплаты'))
async def cmd_about(message: Message):
    text = as_marked_section(
        Bold('Варианты оплаты:'),
        'Картой в боте',
        'При получении карта/кеш',
        'В заведении',
        marker = '✅ '
    )
    await message.answer(text.as_html())

@private_router.message(or_f(Command('shipping'), F.text.lower() == 'вариванты доставки'))
async def cmd_about(message: Message):
    text = as_list(
        as_marked_section(
            Bold('Можно сделать:'),
            'Курьер',
            'Самовывоз',
            'Поем у вас',
            marker =  '✅ '
        ),
        as_marked_section(
            Bold('Нельзя сделать:'),
            'Голуби',
            'Пингвины',
            marker = '❎ '
        ),
        sep = '\n----------------------------------\n'
    )
    await message.answer(text.as_html())


    