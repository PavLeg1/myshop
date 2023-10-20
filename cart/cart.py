from decimal import Decimal
from django.conf import settings
from shop.models import Product


# Класс, управляющий корзиной покупок
class Cart:
    def __init__(self, request):
        # Инициализируем картину

        self.session = request.session

        # Попытка получить корзину из текущего сеанса
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Создаем пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    
    def add(self, product, quantity=1, override_quantity=False):
        # Добавить товар в корзину или обновить его количество

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сеанс как измененный для сохранения
        self.session.modified = True

    def remove(self, product):
        # Удалить товар из корзины

        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        # Прокрутить товары корзины в цикле и получить товары из БД

        product_ids = self.cart.keys()
        # Получить объекты product и добавить их в корзину
        products = Product.objects.filter(id___in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        # Подсчитать все товары в корзине

        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # Очистка корзины

        del self.session[settings.CART_SESSION_ID]
        self.save()