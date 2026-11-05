from typing import List, Dict, Any, Optional


def filter_by_state(data: List[Dict[str, Any]], state: str = "EXECUTED") -> List[Dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'.
    """
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], descending: bool = True) -> List[Dict[str, Any]]:
    """
    Сортирует список словарей по значению ключа 'date'.

    :param data: Список словарей для сортировки.
    :param descending: Если True (по умолчанию), сортировка идет от новых дат к старым (убывание).
                       Если False — от старых к новым (возрастание).
    :return: Новый список отсортированных словарей.
    """
    # Используем sorted() для создания нового списка.
    # Ключ date извлекается через .get() для защиты от KeyError.
    # Если дата отсутствует, возвращается пустая строка, такие элементы окажутся в начале
    # при сортировке по возрастанию и в конце при сортировке по убыванию.
    return sorted(data, key=lambda x: x.get("date", ""), reverse=descending)
