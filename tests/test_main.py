import json
import pytest
from main import (
    Product,
    Category,
    Order,
    ZeroQuantityError,
    load_data_from_json,
)


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0


# --- Старые базовые тесты ---
def test_product_str():
    product = Product("Смартфон", "Хороший", 15000.0, 10)
    assert str(product) == "Смартфон, 15000.0 руб. Остаток: 10 шт."


def test_category_str():
    p1 = Product("Товар 1", "Описание 1", 50.0, 10)
    category = Category("Электроника", "Описание", [p1])
    assert str(category) == "Электроника, количество продуктов: 10 шт."


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
                    "quantity": 1,
                }
            ],
        }
    ]
    file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    categories = load_data_from_json(file_path)
    assert len(categories) == 1


# --- НОВЫЕ ТЕСТЫ (ДЗ 16.3) ---
def test_product_zero_quantity_init():
    """Тест: создание товара с нулевым количеством
     выбрасывает ValueError (Задание 1)."""
    with pytest.raises(ValueError,
                       match="Товар с нулевым количеством не может быть добавлен"):
        Product("Товар", "Описание", 100.0, 0)


def test_average_price_with_products():
    """Тест: подсчет среднего ценника (Задание 2)."""
    p1 = Product("Товар 1", "Описание", 100.0, 1)
    p2 = Product("Товар 2", "Описание", 200.0, 1)
    cat = Category("Кат", "Описание", [p1, p2])
    # (100 + 200) / 2 = 150
    assert cat.average_price() == 150.0


def test_average_price_empty_category():
    """Тест: подсчет среднего ценника в пустой категории (Задание 2)."""
    cat = Category("Пустая", "Описание", [])
    assert cat.average_price() == 0


def test_add_product_zero_quantity(capsys):
    """Тест: добавление товара с нулевым
     количеством через add_product (Доп. задание)."""
    cat = Category("Кат", "Описание")
    p = Product("Товар", "Описание", 100.0, 1)
    p.quantity = 0
    """Искусственно обнуляем, так как __init__ не даст создать такой объект"""

    cat.add_product(p)

    captured = capsys.readouterr()
    assert "Ошибка: Товар с нулевым количеством не может быть добавлен" in captured.out
    assert "Обработка добавления товара завершена" in captured.out


def test_add_product_success(capsys):
    """Тест: успешное добавление товара (Доп. задание)."""
    cat = Category("Кат", "Описание")
    p = Product("Товар", "Описание", 100.0, 1)

    cat.add_product(p)

    captured = capsys.readouterr()
    assert "Товар 'Товар' успешно добавлен" in captured.out
    assert "Обработка добавления товара завершена" in captured.out


def test_order_zero_quantity():
    """Тест: создание заказа с нулевым количеством (Доп. задание)."""
    p = Product("Товар", "Описание", 100.0, 1)
    with pytest.raises(ZeroQuantityError):
        Order(p, 0)
