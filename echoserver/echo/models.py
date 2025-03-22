from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class Book(models.Model):
    id = models.AutoField(primary_key=True)  # Добавляем явное поле id
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'book'  # Указываем имя таблицы в базе данных
    def __str__(self):
        return self.title

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')], default='user')

    def __str__(self):
        return self.username