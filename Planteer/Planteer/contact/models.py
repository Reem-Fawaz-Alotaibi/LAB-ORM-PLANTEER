from django.db import models
from django.core.validators import MinLengthValidator


class Contact(models.Model):
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    message = models.TextField(validators=[MinLengthValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"