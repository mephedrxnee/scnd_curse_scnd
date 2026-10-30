import json
from unittest.mock import patch
import pytest
from main import Product, Category, load_data_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сброс счетчиков перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    product = Product("Товар", "Описание", 100.0, 5)
    assert product.name == "Товар"
    assert product.description == "Описание"
    assert product.price == 100.0
    assert product.quantity == 5


def test_category_initialization():
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    category = Category("Категория", "Описание", [p1])
    assert category.name == "Категория"
    # Проверяем приватный атрибут напрямую, так как products теперь возвращает строку
    assert len(category._Category__products) == 1
    assert Category.product_count == 1


def test_add_product():
    """Тест метода добавления товара в категорию."""
    category = Category("Пустая", "Описание")
    p1 = Product("Новый товар", "Описание", 100.0, 2)

    category.add_product(p1)

    assert len(category._Category__products) == 1
    assert Category.product_count == 1


def test_category_products_getter():
    """Тест геттера products."""
    p1 = Product("Смартфон", "Хороший", 50000.0, 10)
    category = Category("Электроника", "Описание", [p1])

    expected_string = "Смартфон, 50000.0 руб. Остаток: 10 шт.\n"
    assert category.products == expected_string


def test_new_product_classmethod():
    """Тест класс-метода new_product."""
    data = {
        "name": "Ноутбук",
        "description": "Мощный",
        "price": 80000.0,
        "quantity": 3
    }

    product = Product.new_product(data)

    assert isinstance(product, Product)
    assert product.name == "Ноутбук"
    assert product.price == 80000.0


def test_new_product_with_duplicates():
    """Тест доп. задания: проверка дубликатов в new_product."""
    p1 = Product("Ноутбук", "Старый", 80000.0, 3)
    products_list = [p1]

    data = {
        "name": "Ноутбук",
        "description": "Новый",
        "price": 90000.0,
        "quantity": 2
    }

    product = Product.new_product(data, products_list)

    assert product == p1
    assert product.quantity == 5
    assert product.price == 90000.0


def test_price_setter_positive():
    """Тест сеттера цены при положительном значении."""
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = 150.0
    assert product.price == 150.0


def test_price_setter_negative(capsys):
    """Тест сеттера цены при нулевом или отрицательном значении."""
    product = Product("Товар", "Описание", 100.0, 1)

    product.price = -50.0

    assert product.price == 100.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


@patch('builtins.input', return_value='y')
def test_price_setter_lower_with_confirmation(mock_input):
    """Тест доп. задания: понижение цены с подтверждением 'y'."""
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = 50.0
    assert product.price == 50.0


@patch('builtins.input', return_value='n')
def test_price_setter_lower_without_confirmation(mock_input):
    """Тест доп. задания: отказ от понижения цены 'n'."""
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = 50.0
    assert product.price == 100.0


def test_load_data_from_json(tmp_path):
    """Тест загрузки данных из JSON."""
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
    # Снова проверяем приватный атрибут, так как products - это строка
    assert len(categories[0]._Category__products) == 1
