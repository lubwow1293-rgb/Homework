import pytest

from src.widget import get_date, mask_account_card

# Фикстуры для входных данных


@pytest.fixture
def valid_account_card_data() -> list[tuple[str, str]]:
    """Фикстура для валидных данных счета и карты."""
    return [
        # Счета
        ("Счет 1234567890", "Счет *******890"),
        ("Счет 123", "Счет 123"),
        ("Счет 12345678901234567890", "Счет *****************890"),
        # Карты
        ("Visa 1234567890123456", "Visa ************ 3456"),
        ("MasterCard 1111 2222 3333 4444", "MasterCard ************ 4444"),
        ("Maestro 1234-5678-9012-3456", "Maestro ************ 3456"),
    ]


@pytest.fixture
def invalid_card_data_widget() -> list[tuple[str, str]]:
    """Фикстура для невалидных данных карты."""
    return [
        ("Visa", "IndexError"),  # Нет номера карты
        ("Visa ", "IndexError"),  # Пробел, но нет номера
    ]


@pytest.fixture
def valid_date_data() -> list[tuple[str, str]]:
    """Фикстура для валидных данных даты."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2000-01-01T00:00:00.000000", "01.01.2000"),
    ]


@pytest.fixture
def invalid_date_data() -> list[tuple[str, str]]:
    """Фикстура для невалидных данных даты."""
    return [
        ("11.03.2024", "ValueError"),  # Неверный формат
        ("2024-13-01T00:00:00.000000", "ValueError"),  # Неверный месяц
        ("2024-02-30T00:00:00.000000", "ValueError"),  # Неверный день
    ]


# Параметризованные тесты для функции mask_account_card

@pytest.mark.parametrize("input_str, expected", [
    # Счета
    ("Счет 1234567890", "Счет *******890"),
    ("Счет 123", "Счет 123"),
    ("Счет 12345678901234567890", "Счет *****************890"),
    # Карты
    ("Visa 1234567890123456", "Visa ************ 3456"),
    ("MasterCard 1111 2222 3333 4444", "MasterCard ************ 4444"),
    ("Maestro 1234-5678-9012-3456", "Maestro ************ 3456"),
])
def test_mask_account_card_valid(input_str: str, expected: str) -> None:
    """Проверка корректного маскирования валидных счетов и карт."""
    assert mask_account_card(input_str) == expected


@pytest.mark.parametrize("input_str, expected_exception", [
    ("Visa", "IndexError"),  # Нет номера карты
    ("Visa ", "IndexError"),  # Пробел, но нет номера
])
def test_mask_account_card_invalid(input_str: str, expected_exception: str) -> None:
    """Проверка обработки некорректного ввода."""
    with pytest.raises(eval(expected_exception)):
        mask_account_card(input_str)

# Параметризованные тесты для функции get_date


@pytest.mark.parametrize("input_str, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
    ("2000-01-01T00:00:00.000000", "01.01.2000"),
])
def test_get_date_valid(input_str: str, expected: str) -> None:
    """Проверка корректного форматирования даты."""
    assert get_date(input_str) == expected


@pytest.mark.parametrize("input_str, expected_exception", [
    ("11.03.2024", "ValueError"),  # Неверный формат
    ("2024-13-01T00:00:00.000000", "ValueError"),  # Неверный месяц
    ("2024-02-30T00:00:00.000000", "ValueError"),  # Неверный день
])
def test_get_date_invalid_format(input_str: str, expected_exception: str) -> None:
    """Проверка выброса ошибки при неверном формате даты."""
    with pytest.raises(eval(expected_exception)):
        get_date(input_str)
