from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.username