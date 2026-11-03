import json
from unittest.mock import patch
import pytest
<<<<<<< HEAD
from main import Product, Category, CategoryIterator, load_data_from_json
=======
from main import Product, Category, load_data_from_json
>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046


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


def test_product_str():
    """Тест __str__ для Product (Задание 1)."""
    product = Product("Смартфон", "Хороший", 15000.0, 10)
    expected = "Смартфон, 15000.0 руб. Остаток: 10 шт."
    assert str(product) == expected


def test_product_add():
    """Тест __add__ для Product (Задание 2)."""
    p1 = Product("Товар А", "Описание", 100.0, 10)  # 100 * 10 = 1000
    p2 = Product("Товар Б", "Описание", 200.0, 2)  # 200 * 2 = 400

    assert p1 + p2 == 1400.0


def test_category_initialization():
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    category = Category("Категория", "Описание", [p1])
    assert category.name == "Категория"
<<<<<<< HEAD
    assert len(category._Category__products) == 1


def test_category_str():
    """Тест __str__ для Category (Задание 1)."""
    p1 = Product("Товар 1", "Описание 1", 50.0, 10)
    p2 = Product("Товар 2", "Описание 2", 100.0, 5)
    category = Category("Электроника", "Описание", [p1, p2])

    # Общее количество: 10 + 5 = 15
    expected = "Электроника, количество продуктов: 15 шт."
    assert str(category) == expected


def test_category_products_getter():
    """Тест геттера products."""
    p1 = Product("Смартфон", "Хороший", 50000.0, 10)
    category = Category("Электроника", "Описание", [p1])

    expected_string = "Смартфон, 50000.0 руб. Остаток: 10 шт.\n"
    assert category.products == expected_string


def test_category_iterator():
    """Тест итератора (Доп. задание)."""
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    p2 = Product("Товар 2", "Описание 2", 100.0, 2)
    category = Category("Категория", "Описание", [p1, p2])

    iterator = CategoryIterator(category)
    products = list(iterator)

    assert len(products) == 2
    assert products[0] == p1
    assert products[1] == p2


def test_add_product():
    category = Category("Пустая", "Описание")
    p1 = Product("Новый товар", "Описание", 100.0, 2)

    category.add_product(p1)
    assert len(category._Category__products) == 1


def test_new_product_classmethod():
    data = {"name": "Ноутбук", "description": "Мощный", "price": 80000.0, "quantity": 3}
    product = Product.new_product(data)
    assert product.name == "Ноутбук"


def test_new_product_with_duplicates():
    p1 = Product("Ноутбук", "Старый", 80000.0, 3)
    products_list = [p1]
    data = {"name": "Ноутбук", "description": "Новый", "price": 90000.0, "quantity": 2}

    product = Product.new_product(data, products_list)
=======
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

>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046
    assert product == p1
    assert product.quantity == 5
    assert product.price == 90000.0


def test_price_setter_positive():
<<<<<<< HEAD
=======
    """Тест сеттера цены при положительном значении."""
>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = 150.0
    assert product.price == 150.0


def test_price_setter_negative(capsys):
<<<<<<< HEAD
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = -50.0
=======
    """Тест сеттера цены при нулевом или отрицательном значении."""
    product = Product("Товар", "Описание", 100.0, 1)

    product.price = -50.0

>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046
    assert product.price == 100.0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


@patch('builtins.input', return_value='y')
def test_price_setter_lower_with_confirmation(mock_input):
<<<<<<< HEAD
=======
    """Тест доп. задания: понижение цены с подтверждением 'y'."""
>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = 50.0
    assert product.price == 50.0


@patch('builtins.input', return_value='n')
def test_price_setter_lower_without_confirmation(mock_input):
<<<<<<< HEAD
=======
    """Тест доп. задания: отказ от понижения цены 'n'."""
>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046
    product = Product("Товар", "Описание", 100.0, 1)
    product.price = 50.0
    assert product.price == 100.0


def test_load_data_from_json(tmp_path):
<<<<<<< HEAD
    file_path = tmp_path / "test.json"
    data = [{
        "name": "Смартфоны", "description": "Описание",
        "products": [{"name": "Товар", "description":
            "Описание", "price": 10.0, "quantity": 1}]
    }]
=======
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
>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_data_from_json(file_path)
    assert len(categories) == 1
<<<<<<< HEAD
=======
    # Снова проверяем приватный атрибут, так как products - это строка
    assert len(categories[0]._Category__products) == 1
>>>>>>> acaadf2308fb9195995ba79f9e65d6e9f558d046
