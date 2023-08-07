from .models import User,SubUser,Bookshop,Restaurants,Clinics,Petshop
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    
    def create(self,validated_data):
            password = validated_data.pop('password')
            user = User(**validated_data)
            user.password = make_password(password)
            user.save()
            return user

    class Meta:
        model = User
        fields = ['id', 'username','first_name','last_name', 'email', 'role', 'mobile_no', 'date_of_birth', 'gender','password']

        extra_kwargs = {'password':{'write_only':True}}

        
        


class SubUserserializer(serializers.ModelSerializer):
    class Meta:
       model = SubUser 
       fields = ['id', 'username', 'password', 'created_by']
       extra_kwargs = {'password':{'write_only':True}}

    def validate_username(self, value):
        if SubUser.objects.filter(username=value).exists():
            raise serializers.ValidationError({'username': 'This username already exists'})
        return value

     

class Bookserializer(serializers.ModelSerializer):
     class Meta:
          model = Bookshop
          fields = "__all__"

class Restaurantserializer(serializers.ModelSerializer):
     class Meta:
          model = Restaurants
          fields = "__all__"

class Clinicserializer(serializers.ModelSerializer):
     class Meta:
          model = Clinics
          fields = "__all__"

class Petserializer(serializers.ModelSerializer):
     class Meta:
          model = Petshop
          fields ="__all__"