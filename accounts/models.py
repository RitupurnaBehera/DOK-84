from django.db import models
from django.utils import timezone





# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)


    def __str__(self) -> str:
        return self.name

class User(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    username = models.CharField(max_length=200,unique=True)
    firstname = models.CharField(max_length=100,default='')
    lastname = models.CharField(max_length = 100,default='')
    email = models.EmailField(unique=True)
    password1 = models.CharField(max_length=150)
    password2 = models.CharField(max_length=150,default='')
    mobile_no = models.CharField(max_length=10,default='',unique=True)
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

    def __str__(self) -> str:
        return self.username