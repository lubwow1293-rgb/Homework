import re
from datetime import datetime
from masks import get_mask_card_number, get_mask_account


def mask_account_card(input_string: str) -> str:
    """
    Принимает строку вида "Тип карты/счета Номер",
    определяет тип данных и применяет соответствующую маску,
    используя функции из модуля masks.py.
    """
    # Находим первую цифру, чтобы отделить тип от номера
    match = re.search(r'\d', input_string)

    if not match:
        raise ValueError("В строке не найден номер карты или счета")

    # Разделяем строку
    type_part = input_string[:match.start()].strip()
    number_part = input_string[match.start():].strip()

    # Делегируем маскировку функциям из masks.py
    if 'счет' in type_part.lower():
        masked_number = get_mask_account(number_part)
    else:
        masked_number = get_mask_card_number(number_part)

    return f"{type_part} {masked_number}"


def get_date(date_str: str) -> str:
    """
    Функция принимает строку с датой в формате "YYYY-MM-DDTHH:mm:ss.SSSSSS"
    и возвращает её в формате "DD.MM.YYYY".
    """
    # Парсим строку в объект datetime
    parsed_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")

    # Возвращаем форматированную строку
    return parsed_date.strftime("%d.%m.%Y")
