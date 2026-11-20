import json
from abc import ABC, abstractmethod


class ZeroQuantityError(Exception):
    """Пользовательское исключение для товаров с нулевым количеством."""
    pass


class BaseProduct(ABC):
    """Базовый абстрактный класс для продуктов."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        if quantity == 0:
            raise ValueError(
                "Товар с нулевым количеством не может быть добавлен"
            )
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            answer = input("Вы уверены, что хотите понизить цену? (y/n): ")
            if answer.lower() == "y":
                self.__price = new_price
        else:
            self.__price = new_price

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __add__(self, other: "BaseProduct") -> float:
        pass

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: list = None
    ) -> "BaseProduct":
        if products_list:
            for p in products_list:
                if p.name == product_data["name"]:
                    p.quantity += product_data["quantity"]
                    p.price = max(p.price, product_data["price"])
                    return p

        return cls(
            product_data["name"],
            product_data["description"],
            product_data["price"],
            product_data["quantity"],
        )


class ReprMixin:
    """Миксин для вывода информации о созданном объекте."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(repr(self))

    def __repr__(self):
        return (
            f"{self.__class__.__name__}('{self.name}', "
            f"'{self.description}', {self.price}, {self.quantity})"
        )


class Product(ReprMixin, BaseProduct):
    """Класс товара."""

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "BaseProduct") -> float:
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return (self.price * self.quantity) + (other.price * other.quantity)


class Smartphone(Product):
    def __init__(
        self, name: str, description: str, price: float, quantity: int,
        efficiency: float, model: str, memory: int, color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self, name: str, description: str, price: float, quantity: int,
        country: str, germination_period: str, color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class BaseEntity(ABC):
    """Базовый абстрактный класс для Категории и Заказа."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def __str__(self) -> str:
        pass


class Category(BaseEntity):
    """Класс категории."""

    category_count = 0
    product_count = 0

    def __init__(
        self, name: str, description: str, products: list = None
    ) -> None:
        super().__init__(name)
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: Product) -> None:
        """Добавление товара с обработкой исключений (Доп. задание)."""
        try:
            if not isinstance(product, Product):
                raise TypeError(
                    "Можно добавлять только объекты класса Product "
                    "и его наследников"
                )
            if product.quantity == 0:
                raise ZeroQuantityError(
                    "Товар с нулевым количеством не может быть добавлен"
                )
        except (ZeroQuantityError, TypeError) as e:
            print(f"Ошибка: {e}")
        else:
            self.__products.append(product)
            Category.product_count += 1
            print(f"Товар '{product.name}' успешно добавлен")
        finally:
            print("Обработка добавления товара завершена")

    def average_price(self) -> float:
        """Подсчет среднего ценника всех товаров (Задание 2)."""
        try:
            total_price = sum(p.price for p in self.__products)
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0

    @property
    def products(self) -> str:
        return "".join(f"{p}\n" for p in self.__products)


class Order(BaseEntity):
    """Класс заказа."""

    def __init__(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise TypeError("В заказ можно добавить только объект Product")
        if quantity == 0:
            raise ZeroQuantityError(
                "Товар с нулевым количеством не может быть добавлен"
            )
        super().__init__(f"Заказ на {product.name}")
        self.product = product
        self.quantity = quantity
        self.total_cost = product.price * quantity

    def __str__(self) -> str:
        return (
            f"{self.name}, Количество: {self.quantity} шт., "
            f"Итоговая стоимость: {self.total_cost} руб."
        )


class CategoryIterator:
    def __init__(self, category: Category) -> None:
        self.category = category
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.category._Category__products):
            product = self.category._Category__products[self.index]
            self.index += 1
            return product
        raise StopIteration


def load_data_from_json(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for cat_data in data:
        products = []
        for prod_data in cat_data.get("products", []):
            product = Product(
                name=prod_data["name"],
                description=prod_data["description"],
                price=prod_data["price"],
                quantity=prod_data["quantity"],
            )
            products.append(product)

        category = Category(
            name=cat_data["name"],
            description=cat_data["description"],
            products=products,
        )
        categories.append(category)

    return categories
