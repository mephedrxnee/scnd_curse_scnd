import json
import pytest
from main import (
    BaseProduct,
    Product,
    Smartphone,
    LawnGrass,
    BaseEntity,
    Category,
    Order,
    CategoryIterator,
    load_data_from_json,
)


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0


def test_product_str():
    product = Product("Смартфон", "Хороший", 15000.0, 10)
    assert str(product) == "Смартфон, 15000.0 руб. Остаток: 10 шт."


def test_category_str():
    p1 = Product("Товар 1", "Описание 1", 50.0, 10)
    category = Category("Электроника", "Описание", [p1])
    assert str(category) == "Электроника, количество продуктов: 10 шт."


def test_category_iterator():
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    category = Category("Категория", "Описание", [p1])
    assert list(CategoryIterator(category))[0] == p1


def test_add_different_types_raises_error():
    phone = Smartphone(
        "iPhone", "Хороший", 100000.0, 2, 9.5, "15 Pro", 256, "Black"
    )
    grass = LawnGrass(
        "Трава", "Зеленая", 500.0, 100, "Россия", "10 дней", "Green"
    )
    with pytest.raises(TypeError):
        phone + grass


def test_add_product_invalid_raises_error():
    category = Category("Электроника", "Описание")
    with pytest.raises(TypeError):
        category.add_product("Просто строка")


def test_base_product_is_abstract():
    with pytest.raises(TypeError):
        BaseProduct("Товар", "Описание", 100.0, 5)


def test_base_entity_is_abstract():
    with pytest.raises(TypeError):
        BaseEntity("Имя")


def test_repr_mixin(capsys):
    Product("Товар", "Описание", 100.0, 5)
    captured = capsys.readouterr()
    assert "Product('Товар', 'Описание', 100.0, 5)" in captured.out


def test_order_creation():
    p = Product("Товар", "Описание", 100.0, 5)
    order = Order(p, 2)
    assert order.total_cost == 200.0
    assert "Заказ на Товар" in str(order)
    assert "Итоговая стоимость: 200.0 руб." in str(order)


def test_order_invalid_product():
    with pytest.raises(TypeError):
        Order("Не продукт", 2)


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
