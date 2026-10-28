import pytest

from main import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """
    Фикстура для сброса счетчиков класса перед каждым тестом,
    чтобы тесты не зависели друг от друга.
    """
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization():
    """Проверка корректности инициализации объектов класса Product."""
    product = Product("Тестовый товар", "Описание", 100.0, 5)
    assert product.name == "Тестовый товар"
    assert product.description == "Описание"
    assert product.price == 100.0
    assert product.quantity == 5


def test_category_initialization():
    """Проверка корректности инициализации объектов класса Category."""
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    p2 = Product("Товар 2", "Описание 2", 150.0, 2)

    category = Category("Тестовая категория", "Описание категории", [p1, p2])

    assert category.name == "Тестовая категория"
    assert category.description == "Описание категории"
    assert category.products == [p1, p2]
    assert len(category.products) == 2


def test_category_product_counting():
    """Проверка подсчета количества продуктов и категорий."""
    p1 = Product("Товар 1", "Описание 1", 50.0, 1)
    p2 = Product("Товар 2", "Описание 2", 150.0, 2)
    p3 = Product("Товар 3", "Описание 3", 200.0, 3)

    # Создаем первую категорию с 2 товарами
    Category("Категория 1", "Описание 1", [p1, p2])
    assert Category.category_count == 1
    assert Category.product_count == 2

    # Создаем вторую категорию с 1 товаром
    Category("Категория 2", "Описание 2", [p3])
    assert Category.category_count == 2
    assert Category.product_count == 3

    # Создаем пустую категорию
    Category("Пустая категория", "Описание 3", [])
    assert Category.category_count == 3
    assert Category.product_count == 3
