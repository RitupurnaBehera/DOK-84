from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200,unique=True)
    firstname = models.CharField(max_length=100,default='')
    lastname = models.CharField(max_length = 100,default='')
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=150)
    password2 = models.CharField(max_length=150,default='')
    mobile_no = models.CharField(max_length=10,default='')
    date_of_birth = models.DateField(default=timezone.now)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(
        choices=GENDER_CHOICES,
        default='Other'
    )

    # def __str__(self) -> str:
    #     return self.username