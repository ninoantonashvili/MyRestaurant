from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Dish(models.Model):
    SPICE_LEVELS = [
        (0, 'Not Spicy'),
        (1, 'Mild'),
        (2, 'Medium'),
        (3, 'Spicy'),
        (4, 'Very Spicy'),
    ]
    name = models.CharField(max_length=100)
    spicy = models.IntegerField(choices=SPICE_LEVELS)
    withNut = models.BooleanField()
    isVegetarian = models.BooleanField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    imageUrl = models.URLField(max_length=200)
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.RESTRICT)

    def __str__(self):
        return self.name

class BasketItem(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.RESTRICT)
    itemCount = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.itemCount} x {self.dish.name}'

class Basket(models.Model):
    items = models.ManyToManyField(BasketItem)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Basket with {self.items.count()} items'
