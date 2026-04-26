from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.ImageField(upload_to='countries/')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"


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
    countries = models.ManyToManyField(Country, blank=True)


    def __str__(self)->str:
        return self.name
    

class Comment(models.Model):
    plant=models.ForeignKey(Plant,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    
    def __str__(self)->str:
            return f"{self.user.username} on {self.plant.name}"