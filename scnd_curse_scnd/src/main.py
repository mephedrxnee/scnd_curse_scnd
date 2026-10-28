import json


class Product:
    """Класс для описания товара в магазине."""

    def __init__(
            self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """
        Инициализация товара.
        :param name: Название товара.
        :param description: Описание товара.
        :param price: Цена товара.
        :param quantity: Количество в наличии.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для описания категории товаров."""

    # Атрибуты класса для подсчета
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list) -> None:
        """
        Инициализация категории.
        :param name: Название категории.
        :param description: Описание категории.
        :param products: Список товаров (объектов класса Product).
        """
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Увеличение счетчиков класса при создании экземпляра.
        # Обращаемся именно к классу (Category.атрибут), а не к self,
        # чтобы изменять общую переменную для всех объектов.
        Category.category_count += 1
        Category.product_count += len(self.products)


def load_data_from_json(file_path: str) -> list:
    """
    Дополнительное задание: загрузка данных из JSON файла.
    Создает объекты Category и Product на основе данных из файла.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    categories = []
    for cat_data in data:
        products = []
        for prod_data in cat_data.get('products', []):
            product = Product(
                name=prod_data['name'],
                description=prod_data['description'],
                price=prod_data['price'],
                quantity=prod_data['quantity']
            )
            products.append(product)

        category = Category(
            name=cat_data['name'],
            description=cat_data['description'],
            products=products
        )
        categories.append(category)

    return categories


if __name__ == "__main__":
    # Код из скриншота для проверки работоспособности
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера",
        180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации...",
        [product1, product2, product3]
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор...",
        [product4]
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)