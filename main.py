from aiogram import Bot, Dispatcher, types, executor
import expenses



API_TOKEN = "5783433118:AAGfQBQ_oe8W7vMCguUtKJmj2tkBTsILVUc"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.message):
    """
    This handler will be called when user sends '/start' or '/help' command
    """
    await message.reply(
        "Бот для ведения финансовой отчетности\n\n"
        "Добавить расходы: 300 продукты\n"
        "Получить список доступных категорий: /categories\n"
        "Статистика расходов за день: /today\n"
        "Статистика расходов за месяц: /month\n"
        "Посмотреть последние расходы: /expenses\n"
    )


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет одну запись с расходов по айди"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Удалено!"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Возвращает список доступных категорий"""
    answer_message = "Доступные категори:\n\n* " + ("\n* ".join(expenses.CATEGORIES))
    await message.reply(answer)


@dp.message_handler(commands=['today'])
async def today_statistics(message: types.Message):
    """Возвращает статистику расходов за сегодня"""
    answer_message = expenses.get_today_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_statitics(message: types.Message):
    """Возвращает статистику расходов за месяц"""
    answer_message = expenses.get_month_statistics()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Возвращает несколько последних записей про расходы"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Расходов еще нет")
        return

    last_expenses_rows = [
        f"{expense.amount} грн. на {expense.category} - нажимай /del{expense.id} для удаления"
        for expense in last_expenses]
    answer_message = "Послендние расходы: \n\n* " + "\n\n* ".join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    """Добавляет новые расходы"""
    try:
        expense = expenses.add_expense(message.text)
    except Exception as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Добавим расходы {expense.amount} грн на {expense.category}.\n\n"
        f"{expenses.get_today_statistics()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


