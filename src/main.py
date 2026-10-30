import json


class Product:
    """Класс для описания товара в магазине."""

    def __init__(
            self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        # Делаем цену приватной
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            # Доп. задание: подтверждение понижения цены
            answer = input("Вы уверены, что хотите понизить цену? (y/n): ")
            if answer.lower() == 'y':
                self.__price = new_price
        else:
            self.__price = new_price

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None) -> 'Product':
        """Класс-метод для создания товара из словаря."""
        if products_list:
            for p in products_list:
                if p.name == product_data['name']:
                    # Если товар есть, суммируем количество и берем макс. цену
                    p.quantity += product_data['quantity']
                    p.price = max(p.price, product_data['price'])
                    return p

        return cls(
            product_data['name'],
            product_data['description'],
            product_data['price'],
            product_data['quantity']
        )


class Category:
    """Класс для описания категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None) -> None:
        self.name = name
        self.description = description
        # Делаем список товаров приватным
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def add_product(self, product: Product) -> None:
        """Метод для добавления товара в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для вывода списка товаров в виде строки."""
        result = ""
        for product in self.__products:
            result += (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )
        return result


def load_data_from_json(file_path: str) -> list:
    """Функция загрузки данных из JSON."""
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


if __name__ == "__main__":  # pragma: no cover
    # Проверка работоспособности
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5)
    category1 = Category("Смартфоны", "Описание смартфонов", [product1])
    print(category1.products)
