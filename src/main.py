import json


class Product:
    """Базовый класс для описания товара в магазине."""

    def __init__(
            self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое отображение товара."""
        return (
            f"{self.name}, {self.price} руб. "
            f"Остаток: {self.quantity} шт."
        )

    def __add__(self, other: 'Product') -> float:
        """Магический метод сложения товаров (Задание 2)."""
        # Проверяем, что складываются товары строго одного класса
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")

        total_cost_self = self.price * self.quantity
        total_cost_other = other.price * other.quantity
        return total_cost_self + total_cost_other

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
                    p.quantity += product_data['quantity']
                    p.price = max(p.price, product_data['price'])
                    return p

        return cls(
            product_data['name'],
            product_data['description'],
            product_data['price'],
            product_data['quantity']
        )


class Smartphone(Product):
    """Класс для смартфонов (Задание 1)."""

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            efficiency: float,
            model: str,
            memory: int,
            color: str
    ) -> None:
        # Вызываем конструктор родительского класса
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Класс для газонной травы (Задание 1)."""

    def __init__(
            self,
            name: str,
            description: str,
            price: float,
            quantity: int,
            country: str,
            germination_period: str,
            color: str
    ) -> None:
        # Вызываем конструктор родительского класса
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс для описания категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list = None) -> None:
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self) -> str:
        """Строковое отображение категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Метод для добавления товара в категорию (Задание 3)."""
        # Проверяем, является ли объект экземпляром Product или его наследником
        if not isinstance(product, Product):
            raise (TypeError
                   ("Можно добавлять только объекты класса Product и его наследников"))

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для вывода списка товаров."""
        return "".join(f"{product}\n" for product in self.__products)


class CategoryIterator:
    """Итератор для перебора товаров категории."""

    def __init__(self, category: Category) -> None:
        self.category = category
        self.index = 0

    def __iter__(self) -> 'CategoryIterator':
        return self

    def __next__(self) -> Product:
        if self.index < len(self.category._Category__products):
            product = self.category._Category__products[self.index]
            self.index += 1
            return product
        raise StopIteration


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
