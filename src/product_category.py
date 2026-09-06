from abc import ABC, abstractmethod


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name, description, price, quantity):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.quantity = quantity


class PrintMixin:
    name = str
    description = str
    price = float
    quantity = int

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})"


class Product(BaseProduct, PrintMixin):
    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        self.__price = price

    @classmethod
    def new_product(cls, product_info):
        new_product = cls(**product_info)
        return new_product

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        elif new_price < self.__price:
            confirm = input("Цена товара понижается. Подтвердите изменение (y/n): ")
            if confirm.lower() == "y":
                self.__price = new_price
        else:
            self.__price = new_price

    def __str__(self):
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(other) is type(self):
            return (self.price * self.quantity) + (other.price * other.quantity)
        raise TypeError("Нельзя добавлять товары разных категорий.")


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products) if products is not None else 0

    @property
    def products(self):
        return "\n".join(str(product) for product in self.__products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
            return
        raise TypeError(
            f"Можно добавлять только объекты Product или его наследников! "
            f"Получен тип: {type(product).__name__}"
        )

    def middle_price(self):
        sum_price = 0
        try:
            for product in self.__products:
                sum_price += product.price
            result = sum_price / len(self.__products)
            return result
        except ZeroDivisionError:
            return 0

class Smartphone(Product):
    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


def test_middle_price_with_products():
    product1 = Product("Товар1", "Описание1", 100.0, 5)
    product2 = Product("Товар2", "Описание2", 200.0, 3)
    product3 = Product("Товар3", "Описание3", 150.0, 2)
    category = Category("Электроника", "Техника", [product1, product2, product3])

    expected = (100.0 + 200.0 + 150.0) / 3
    assert category.middle_price() == expected


def test_middle_price_single_product():
    product = Product("Товар", "Описание", 100.0, 5)
    category = Category("Категория", "Описание", [product])
    assert category.middle_price() == 100.0


def test_middle_price_empty_category():
    category = Category("Пустая", "Нет товаров", [])
    assert category.middle_price() == 0


def test_middle_price_with_inherited_products():
    smartphone = Smartphone("Samsung", "Смартфон", 800.0, 3, "высокая", "S23", "128GB", "черный")
    grass = LawnGrass("Трава", "Газонная", 50.0, 100, "Россия", "14 дней", "зеленый")
    category = Category("Смесь", "Разные товары", [smartphone, grass])
    expected = (800.0 + 50.0) / 2
    assert category.middle_price() == expected


def test_middle_price_no_side_effects():
    product = Product("Товар", "Описание", 100.0, 5)
    category = Category("Категория", "Описание", [product])
    original_products = category._Category__products[:]  # копия списка
    category.middle_price()
    assert category._Category__products == original_products