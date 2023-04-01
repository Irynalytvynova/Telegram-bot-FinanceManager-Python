import datetime
import pytz

from typing import List, NamedTuple, Optional

import db

CATEGORIES = ("продукты", "кафе и рестораны", "такси", "дом", "путешествия")


class Message(NamedTuple):
    """Структура полученного сообщения"""
    amount: int
    category: str


class Expense(NamedTuple):
    """Структура расходов"""
    id: Optional[int]
    amount: int
    category: str


def add_expense(raw_message: str) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)

    today_datetime = _get_current_datetime()
    created = today_datetime.strftime("%Y-%m-%d %H:%M:%S")

    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": created,
        "category": parsed_message.category,
    })
    return Expense(id=None, amount=parsed_message.amount,category=parsed_message.category)


def get_today_statistics() -> str:
    """Возвращает списов расходов за сегодня"""
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   "from expense where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "За сегодня нет расходов"

    return (f"Расходы за сегодня:\n"
            f"Всего - {result[0]} грн.")


def get_month_statistics() -> str:
    """Возвращает список расходов за месяц"""
    now = _get_current_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) "
                   f"from expense where date(created) >= '{first_day_of_month}'")

    result = cursor.fetchone()
    if not result[0]:
        return "В этом месяце нет расходов"

    return (f"Расходы в поточном месяце:\n"
            f"Всего - {result[0]} грн.")

def last() -> List[Expense]:
    """Возвращает несколько последних расходов"""
    cursor = db.get_cursor()
    cursor.execute(
        "select expense.id, expense.amount, expense.category "
        "from expense "
        "order by created desc limit 10")
    rows = cursor.fetchall()
    last_expense = [Expense(id=row[0], amount=row[1], category=row[2]) for row in rows]
    return last_expenses


def delete_expense(row_id: int) -> None:
    """удаляет расходы по айди"""
    db.delete("expense", row_id)


def _parse_message(raw_message:str) -> Message:
    """Парсить текс сообщения"""
    amount, category = raw_message.split(maxsplit=1)
    if category not in CATEGORIES:
        raise Exception(f"Котегории '{category}' не существует")

    return Message(amount=amount, category=category)

def _get_current_datetime():
    tz = pytz.timezone("Europe/Kiev")
    today_datetime = datetime.datetime.now(tz)
    return today_datetime

















