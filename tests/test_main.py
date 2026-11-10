import json
from unittest.mock import patch
import pytest
from main import (
    Product, Category, CategoryIterator,
    Smartphone, LawnGrass, load_data_from_json
)


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сброс счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


# --- Тесты базовых классов (из прошлых ДЗ) ---
def test_product_initialization():
    product = Product("Товар", "Описание", 100.0, 5)
    assert product.name == "Товар"
    assert product.price == 100.0


def test_product_str():
    product = Product("Смартфон", "Хороший", 15000.0, 10)
    assert str(product) == "Смартфон, 15000.0 руб. Остаток: 10 шт."


def test_category_initialization():
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    category = Category("Категория", "Описание", [p1])
    assert category.name == "Категория"
    assert len(category._Category__products) == 1


def test_category_str():
    p1 = Product("Товар 1", "Описание 1", 50.0, 10)
    category = Category("Электроника", "Описание", [p1])
    assert str(category) == "Электроника, количество продуктов: 10 шт."


def test_category_products_getter():
    p1 = Product("Смартфон", "Хороший", 50000.0, 10)
    category = Category("Электроника", "Описание", [p1])
    assert category.products == "Смартфон, 50000.0 руб. Остаток: 10 шт.\n"


def test_category_iterator():
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    category = Category("Категория", "Описание", [p1])
    assert list(CategoryIterator(category))[0] == p1


def test_new_product_with_duplicates():
    p1 = Product("Ноутбук", "Старый", 80000.0, 3)
    data = {"name": "Ноутбук", "description": "Новый", "price": 90000.0, "quantity": 2}
    product = Product.new_product(data, [p1])
    assert product == p1
    assert product.quantity == 5
    assert product.price == 90000.0


@patch('builtins.input', return_value='y')
def test_price_setter_lower_with_confirmation(mock_input):
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = 50.0
    assert product.price == 50.0


def test_load_data_from_json(tmp_path):
    file_path = tmp_path / "test.json"
    data = [
        {
            "name": "Смартфоны",
            "description": "Описание",
            "products": [
                {
                    "name": "Товар",
                    "description": "Описание",
                    "price": 10.0,
                    "quantity": 1
                }
            ]
        }
    ]
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    categories = load_data_from_json(file_path)
    assert len(categories) == 1


# --- НОВЫЕ ТЕСТЫ (ДЗ 16.1) ---
def test_smartphone_initialization():
    """Тест создания смартфона."""
    phone = Smartphone(
        "iPhone", "Хороший", 100000.0, 5,
        efficiency=9.5, model="15 Pro", memory=256, color="Black"
    )
    assert phone.name == "iPhone"
    assert phone.efficiency == 9.5
    assert phone.model == "15 Pro"
    assert phone.memory == 256
    assert phone.color == "Black"
    assert isinstance(phone, Product)  # Проверка наследования


def test_lawngrass_initialization():
    """Тест создания газонной травы."""
    grass = LawnGrass(
        "Трава", "Зеленая", 500.0, 100,
        country="Россия", germination_period="10 дней", color="Green"
    )
    assert grass.name == "Трава"
    assert grass.country == "Россия"
    assert grass.germination_period == "10 дней"
    assert grass.color == "Green"
    assert isinstance(grass, Product)  # Проверка наследования


def test_add_same_types():
    """Тест сложения товаров одного класса."""
    phone1 = Smartphone("iPhone", "Хороший", 100000.0, 2, 9.5, "15 Pro", 256, "Black")
    phone2 = Smartphone("Samsung", "Отличный", 80000.0, 3, 9.0, "S23", 128, "White")

    # 100000 * 2 + 80000 * 3 = 200000 + 240000 = 440000
    assert phone1 + phone2 == 440000.0


def test_add_different_types_raises_error():
    """Тест ошибки при сложении разных классов."""
    phone = Smartphone("iPhone", "Хороший", 100000.0, 2, 9.5, "15 Pro", 256, "Black")
    grass = LawnGrass("Трава", "Зеленая", 500.0, 100, "Россия", "10 дней", "Green")

    with pytest.raises(TypeError):
        phone + grass


def test_add_product_valid():
    """Тест добавления наследника Product в категорию."""
    category = Category("Электроника", "Описание")
    phone = Smartphone("iPhone", "Хороший", 100000.0, 2, 9.5, "15 Pro", 256, "Black")

    category.add_product(phone)
    assert len(category._Category__products) == 1


def test_add_product_invalid_raises_error():
    """Тест ошибки при добавлении не-Product в категорию."""
    category = Category("Электроника", "Описание")

    with pytest.raises(TypeError):
        category.add_product("Просто строка")
