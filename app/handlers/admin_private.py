from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app.filters import filterForChats, IsAdmin
from app.keyboards.reply_keyboards import get_keyboard

admin_router = Router()
admin_router.message.filter(filterForChats(["private"]), IsAdmin())

class Addproduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'Addproduct:name': 'Введите название заново',
        'Addproduct:description': 'Введите описание товара заново',
        'Addproduct:price': 'Введите цену товара заново',
        'Addproduct:image': '...'
    }

ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Изменить товар",
    "Удалить товар",
    "Я так, просто посмотреть зашел",
    placeholder="Выберите действие",
    sizes=(2, 1, 1),
)

BACK_CANCEL = get_keyboard(
    'Назад',
    'Отмена',
    placeholder = 'Выберите действие', 
)

@admin_router.message(Command("admin"))
async def add_product(message: Message):
    await message.answer("Что хотите сделать?", reply_markup = ADMIN_KB)

@admin_router.message(F.text == "Я так, просто посмотреть зашел")
async def starring_at_product(message: Message):
    await message.answer("ОК, вот список товаров")

@admin_router.message(F.text == "Изменить товар")
async def change_product(message: Message):
    await message.answer("ОК, вот список товаров")

@admin_router.message(F.text == "Удалить товар")
async def delete_product(message: Message):
    await message.answer("Выберите товар(ы) для удаления")

@admin_router.message(StateFilter(None), F.text == 'Добавить товар')
async def add_product(message: Message, state: FSMContext):
    await message.answer(text = 'Введите название товара', reply_markup = BACK_CANCEL)
    await state.set_state(Addproduct.name)    

@admin_router.message(StateFilter('*'), Command('отмена'))
@admin_router.message(StateFilter('*'), F.text.casefold() == 'отмена')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(text = 'Действия отменены', reply_markup = ADMIN_KB)
    
@admin_router.message(Command('назад'))
@admin_router.message(F.text.casefold() == 'назад')
async def cmd_back(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == Addproduct.name:
        await message.answer(text = 'Текущего состояния нет')
        return
    
    previous = None
    for step in Addproduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Вы вернулись к прошлому состоянию {Addproduct.texts[previous.state]}", reply_markup = BACK_CANCEL)
        previous = step

@admin_router.message(Addproduct.name, F.text)
async def cmd_input_name(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    await message.answer(text = 'Введите описание товара')
    await state.set_state(Addproduct.description)

@admin_router.message(Addproduct.description, F.text)
async def cmd_input_discription(message: Message, state: FSMContext):
    await state.update_data(discription = message.text)
    await message.answer(text = 'Введите цену товара')
    await state.set_state(Addproduct.price)

@admin_router.message(Addproduct.price, F.text)
async def cmd_input_price(message: Message, state: FSMContext):
    await state.update_data(price = message.text)
    await message.answer(text = 'Пришлите фото товара')
    await state.set_state(Addproduct.image)

@admin_router.message(Addproduct.image, F.photo)
async def cmd_input_photo(message: Message, state: FSMContext):
    await message.answer(text = 'Товар успешно добавлен', reply_markup = ADMIN_KB)
    await state(image = message.photo[-1].file_id)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()