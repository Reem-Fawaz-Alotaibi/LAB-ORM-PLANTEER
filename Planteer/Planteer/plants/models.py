from django.db import models
from django.core.validators import MinLengthValidator


class Plant(models.Model):

    class Category(models.TextChoices):
        FLOWER = 'flower', 'Flower'
        FRUIT = 'fruit', 'Fruit'
        VEGETABLE = 'vegetable', 'Vegetable'
        HERB = 'herb', 'Herb'
        TREE = 'tree', 'Tree'
        CACTUS = 'cactus', 'Cactus'

    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to='plants/')
    category = models.CharField(max_length=20, choices=Category.choices)
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


