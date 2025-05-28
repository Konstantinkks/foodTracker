import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from config import TOKEN
from db import init_db, add_product, get_products
from notify import scheduler, notify_expiring_products

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👋 Привет! Я помогу тебе вести учёт продуктов.

Используй /add чтобы добавить продукт.
Например:
Молоко, 1 л, 2025-05-30

И /list чтобы посмотреть, что у тебя есть.")

@dp.message(Command("add"))
async def cmd_add(message: Message):
    await message.answer("✍️ Введи продукт в формате:
Название, Кол-во, Срок (ГГГГ-ММ-ДД)")

@dp.message()
async def handle_product_entry(message: Message):
    parts = [x.strip() for x in message.text.split(",")]
    if len(parts) != 3:
        await message.answer("❌ Неверный формат. Пример:
Хлеб, 1 шт, 2025-06-01")
        return
    name, qty, date = parts
    if add_product(message.from_user.id, name, qty, date):
        await message.answer(f"✅ Продукт добавлен: {name} — {qty} до {date}")
    else:
        await message.answer("❌ Ошибка при добавлении. Проверь формат даты (ГГГГ-ММ-ДД)")

@dp.message(Command("list"))
async def cmd_list(message: Message):
    products = get_products(message.from_user.id)
    if not products:
        await message.answer("📭 У тебя пока нет продуктов.")
        return
    lines = ["📋 Список продуктов:"]
    for name, qty, date in products:
        lines.append(f"— {name} ({qty}), до {date}")
    await message.answer("\n".join(lines))

async def main():
    init_db()
    scheduler.start()
    scheduler.add_job(notify_expiring_products, 'interval', hours=24, args=[bot])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())