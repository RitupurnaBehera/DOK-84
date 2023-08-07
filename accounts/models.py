from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser,Permission





# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50,unique=True)


    def __str__(self) -> str:
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(Role,on_delete=models.CASCADE,null=True,default=None)
    # username = models.CharField(max_length=200,unique=True)
    # firstname = models.CharField(max_length=100,default='')
    # lastname = models.CharField(max_length = 100,default='')
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=150)
    # password2 = models.CharField(max_length=150,default='')
    mobile_no = models.CharField(max_length=10,default='',unique=True)
    date_of_birth = models.DateField(default=timezone.now)
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    gender = models.CharField(max_length=10,
        choices=GENDER_CHOICES,
        default='Other'
    )


    

    def __str__(self) -> str:
        return self.username
    

class SubUser(models.Model):
    username = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='sub_users',default=None)

    class Meta:
        db_table = "subuser"
        unique_together = ("username","created_by")


class Bookshop(models.Model):
    name = models.CharField(max_length=200,unique=True)

    
    class Meta:
        permissions = [
            ('can_change_bookshop','can change bookshop'),
        ]

    def __str__(self):
        return self.name

class Restaurants(models.Model):
    name = models.CharField(max_length=200,unique = True)

    class Meta:
        permissions = [
            ('can_change_restaurants','can change restaurants'),
        ]

    def __str__(self):
        return self.name
    
class Clinics(models.Model):
    name = models.CharField(max_length=200,unique=True)

    class Meta:
        permissions = [
            ('can_change_clinics','can change clinics'),
        ]

    def __str__(self):
        return self.name
    
class Petshop(models.Model):
    name = models.CharField(max_length=200,unique=True)

    class Meta:
        permissions = [
            ('can_change_petshop','can change petshop'),
        ]

    def __str__(self):
        return self.name
    



