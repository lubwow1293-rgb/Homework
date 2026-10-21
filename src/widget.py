"""
Функция маскировки номера банковского счета или карты
"""


def mask_account_card(card_or_account_string):
    # Проверяем, является ли входящая строка счётом
    if card_or_account_string.startswith("Счет"):
        # Маскируем счёт: оставляем последние 3 цифры
        prefix = "Счет "
        number_part = card_or_account_string[len(prefix) :]
        masked_number = "*" * (len(number_part) - 3) + number_part[-3:]
        return f"{prefix}{masked_number}"

    # Обрабатываем карту
    else:
        # Разделяем строку по первому пробелу, чтобы отделить название от цифр
        parts = card_or_account_string.split(maxsplit=1)

        # Берём только те символы, которые являются цифрами
        digits_only = "".join(c for c in parts[1] if c.isdigit())

        # Формируем маску вида **** **** **** #### (последние 4 цифры)
        masked_digits = "*" * len(digits_only[:-4]) + " " + digits_only[-4:]

        # Возвращаем результат с сохранением оригинального названия карты
        return f"{parts[0]} {masked_digits.strip()}"
