from django.db import models
from django.urls import reverse

# Состоит из полей name, slug
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name 
    
    # Получаем URL объекта
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])
    
# Состоит из полей:
# category - (внешний ключ) один ко многим - товар - одна категория / категория - несколько товаров 
# name - название товара
# slug - слаг для читаемости URL
# image - опциональное изображение товара
# description - опциональное описание товара
# price - цена (два знака после запятой). ДЛЯ ХРАНЕНИЯ ДЕНЕЖНЫХ СУММ - ВСЕГДА DecimalField
# available - наличие / отсутствие товара
# created - дата/время создания
# updated - дата/время обновления
class Product(models.Model):
    Category = models.ForeignKey(Category,
                                 related_name = 'products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                             decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name
    
    # Получаем URL объекта
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])
    

