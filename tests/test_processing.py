from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date

# Тестовые данные
test_data = [
    {"id": 1, "state": "EXECUTED", "date": "2024-01-15T10:00:00"},
    {"id": 2, "state": "PENDING", "date": "2024-01-14T09:00:00"},
    {"id": 3, "state": "EXECUTED", "date": "2024-01-16T11:00:00"},
    {"id": 4, "state": "CANCELLED", "date": "2024-01-13T08:00:00"},
    {"id": 5, "state": "EXECUTED", "date": "2024-01-12T07:00:00"},
    {"id": 6, "state": "PENDING", "date": "2024-01-17T12:00:00"},
    {"id": 7, "state": "EXECUTED"},  # Без даты
    {"id": 8, "date": "2024-01-18T13:00:00"},  # Без state
    {"id": 9},  # Без state и date
]


# Фикстуры

@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    """Фикстура с тестовыми данными."""
    return test_data


@pytest.fixture
def empty_data() -> List[Dict[str, Any]]:
    """Фикстура с пустым списком."""
    return []


@pytest.fixture
def all_executed_data() -> List[Dict[str, Any]]:
    """Фикстура, где все элементы имеют state='EXECUTED'."""
    return [{"id": i, "state": "EXECUTED"} for i in range(10)]


@pytest.fixture
def no_state_data() -> List[Dict[str, Any]]:
    """Фикстура с элементами без ключа 'state'."""
    return [{"id": 1}, {"id": 2, "state": "EXECUTED"}, {"id": 3}]


@pytest.fixture
def no_date_data() -> List[Dict[str, Any]]:
    """Фикстура с элементами без ключа 'date'."""
    return [{"id": 1}, {"id": 2}, {"id": 3}]


@pytest.fixture
def same_date_data() -> List[Dict[str, Any]]:
    """Фикстура с элементами с одинаковой датой."""
    return [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-01-01"},
        {"id": 3, "date": "2024-01-01"}
    ]


# Тесты для filter_by_state

@pytest.mark.parametrize("state, expected_ids", [
    ("EXECUTED", [1, 3, 5, 7]),
    ("PENDING", [2, 6]),
    ("CANCELLED", [4]),
    ("UNKNOWN", []),
])
def test_filter_by_state_various_state(sample_data: List[Dict[str, Any]], state: str, expected_ids: List[int]) -> None:
    """Проверка фильтрации по разным значениям state."""
    result = filter_by_state(sample_data, state)
    actual_ids = [item["id"] for item in result]
    assert actual_ids == expected_ids


def test_filter_by_state_default(sample_data: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации по умолчанию (state='EXECUTED')."""
    result = filter_by_state(sample_data)
    actual_ids = [item["id"] for item in result]
    assert actual_ids == [1, 3, 5, 7]


def test_filter_by_state_empty(empty_data: List[Dict[str, Any]]) -> None:
    """Проверка фильтрации пустого списка."""
    result = filter_by_state(empty_data)
    assert result == []


def test_filter_by_state_all_match(all_executed_data: List[Dict[str, Any]]) -> None:
    """Проверка, когда все элементы подходят под фильтр."""
    result = filter_by_state(all_executed_data)
    assert len(result) == 10
    assert all(item["state"] == "EXECUTED" for item in result)


def test_filter_by_state_no_state_key(no_state_data: List[Dict[str, Any]]) -> None:
    """Проверка элементов без ключа 'state'."""
    result = filter_by_state(no_state_data, "EXECUTED")
    actual_ids = [item["id"] for item in result]
    assert actual_ids == [2]


# Тесты для sort_by_date

@pytest.mark.parametrize("descending, expected_order", [
    (True, [8, 6, 3, 1, 2, 4, 5, 7, 9]),
    (False, [7, 9, 5, 4, 2, 1, 3, 6, 8]),
])
def test_sort_by_date_various_orders(
    sample_data: List[Dict[str, Any]],
    descending: bool,
    expected_order: List[int],
) -> None:
    """Проверка сортировки по дате в разных направлениях."""
    result = sort_by_date(sample_data, descending=descending)
    actual_order = [item["id"] for item in result]
    assert actual_order == expected_order


def test_sort_by_date_default(sample_data: List[Dict[str, Any]]) -> None:
    """Проверка сортировки по умолчанию (по убыванию)."""
    result = sort_by_date(sample_data)
    actual_order = [item["id"] for item in result]
    assert actual_order == [8, 6, 3, 1, 2, 4, 5, 7, 9]


def test_sort_by_date_ascending(sample_data: List[Dict[str, Any]]) -> None:
    """Проверка сортировки по возрастанию."""
    result = sort_by_date(sample_data, descending=False)
    actual_order = [item["id"] for item in result]
    assert actual_order == [7, 9, 5, 4, 2, 1, 3, 6, 8]


def test_sort_by_date_empty(empty_data: List[Dict[str, Any]]) -> None:
    """Проверка сортировки пустого списка."""
    result = sort_by_date(empty_data)
    assert result == []


def test_sort_by_date_no_date(no_date_data: List[Dict[str, Any]]) -> None:
    """Проверка сортировки элементов без даты."""
    result = sort_by_date(no_date_data)
    actual_order = [item["id"] for item in result]
    assert actual_order == [1, 2, 3]


def test_sort_by_date_same_date(same_date_data: List[Dict[str, Any]]) -> None:
    """Проверка стабильной сортировки при одинаковых датах."""
    result = sort_by_date(same_date_data)
    actual_order = [item["id"] for item in result]
    assert actual_order == [1, 2, 3]


def test_sort_by_date_same_date_descending(same_date_data: List[Dict[str, Any]]) -> None:
    """Проверка стабильной сортировки при одинаковых датах (по убыванию)."""
    result = sort_by_date(same_date_data, descending=True)
    actual_order = [item["id"] for item in result]
    assert actual_order == [1, 2, 3]
