from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User,SubUser,Bookshop,Restaurants,Clinics,Petshop
from django.contrib.auth.models import Permission

from .serializers import UserSerializer,SubUserserializer,Bookserializer,Restaurantserializer,Clinicserializer,Petserializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import CanChangeBookshopPermission,CanChangeRestaurantsPermission,CanChangeClinicsPermission,CanChangePetshopPermission
from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.models import ContentType



# from rest_framework_simplejwt.authentication import JWTAuthentication
class UserRegistrationView(APIView):
    

    def get(self, request):

        queryset = User.objects.get(id=request.data.get('id'))
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def post(self, request):

        password = request.data.get('password')
        password2 = request.data.get('password2') 

        if not password or not password2:
            return Response({'message': 'Please provide password, and password2'}, status=status.HTTP_400_BAD_REQUEST)

        if password != password2:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST) 
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
    
        return Response(serializer.data,status=status.HTTP_201_CREATED)


    def put(self, request):
        user = User.objects.get(id=request.data.get('id'))
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        id = request.data.get('id')
        # username = request.data.get('username')
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete() 
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        # password = request.data.get('password')
        

        if not username :
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user)
        # user = User.objects.get(username = serializer.data['username'])
        refresh = RefreshToken.for_user(user)
        return Response({'payload':serializer.data, 'status':200,'refresh': str(refresh),'access': str(refresh.access_token)})
        
        






        




# Subuser Registration and Login

class subuserregisterAPI(APIView):
    def post(self,request):
        password = request.data.get('password')
        password2 = request.data.get('password2') 

        if not password or not password2:
            return Response({'message': 'Please provide password, and password2'}, status=status.HTTP_400_BAD_REQUEST)

        if password != password2:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST) 
        serializer = SubUserserializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

        serializer.save()
        # user = User.objects.get(username = serializer.data['Username'])
        return Response(serializer.data,status=status.HTTP_201_CREATED)
        # refresh = RefreshToken.for_user(user)
        # return Response({'payload':serializer.data, 'status':200,'refresh': str(refresh),'access': str(refresh.access_token),})
        # # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        
class subuserloginAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            user = SubUser.objects.get(username=username, password=password)
        except SubUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = SubUserserializer(user)
        
        
        return Response(serializer.data, status=status.HTTP_200_OK)
        



#In this,Admin can see all users data


class AdminListView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            
            user_id = request.user.id
            
            if user_id is not None:
                user = User.objects.get(id=user_id)
                if user.role.name == "admin":
                    users = User.objects.all()
                    serializer = UserSerializer(users, many=True)
                    return Response(serializer.data)
                else:
                    return Response(
                        {"message": "You don't have permission to perform actions"},
                        status=status.HTTP_403_FORBIDDEN
                    )
            else:
                return Response(
                    {"error": "Please provide the 'id' parameter in the request data."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except User.DoesNotExist:
            return Response(
                {"error": "User with the provided ID does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )


class SubuserOnlyAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = request.user.id
        if user_id is not None:
            user = User.objects.get(id=user_id)

        if user.role.name=="subuser":
            subuser_data = User.objects.get(id=user_id,created_by__role__name="admin")
            serializer = UserSerializer(subuser_data,many=True)
            return Response(serializer.data)
        
        return Response({"error": "User ID not provided or user is not a subuser of admin"}, status=400)







class AdminDataAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = request.user.id
        if user_id is not None:
            user = User.objects.get(id=user_id)

        if user.role.name == 'admin':
            admin_data = User.objects.filter(role__name='admin')
            subuser_data = User.objects.filter(role__name='subuser',created_by__role__name='admin')
            serializer = UserSerializer(admin_data, many=True)
            serializers = UserSerializer(subuser_data, many=True)
            return Response({"admin_data": serializer.data, "subuser_data": serializers.data})
        return Response({"error": "User ID not provided or user is not an admin."}, status=400)
    





class BookshopAPIIView(APIView):
    permission_classes = [CanChangeBookshopPermission]


    def post(self,request):
        serializer = Bookserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        books = Bookshop.objects.all()
        serializer=Bookserializer(books,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request):
        books = Bookshop.objects.get(id=request.data.get('id'))
        serializer = Bookserializer(books, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

    
class RestaurantsAPIView(APIView):
    permission_classes = [CanChangeRestaurantsPermission]

    def post(self,request):
        serializer = Restaurantserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        restaurants = Restaurants.objects.all()
        serializer=Restaurantserializer(restaurants,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request):
        restaurants = Restaurants.objects.get(id=request.data.get('id'))
        serializer = Restaurantserializer(restaurants, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ClinicsAPIView(APIView):
    permission_classes = [CanChangeClinicsPermission]
    def post(self,request):
        serializer = Clinicserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        clinics = Clinics.objects.all()
        serializer=Clinicserializer(clinics,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request):
        clinics = Clinics.objects.get(id=request.data.get('id'))
        serializer = Clinicserializer(clinics, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PetsAPIView(APIView):
    permission_classes = [CanChangePetshopPermission]
    def post(self,request):
        serializer =Petserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def get(self, request):
        petshop = Petshop.objects.all()
        serializer=Petserializer(petshop,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
      
    def put(self, request):
        petshop = Petshop.objects.get(id=request.data.get('id'))
        serializer = Petserializer(petshop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#assigning permissions

class AssignPermission(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user making the request is a superuser
        if not request.user.is_superuser:
            return Response({"message": "You don't have permission to assign permissions."},
                            status=status.HTTP_403_FORBIDDEN)

        username = request.data.get('username')
        model_name = request.data.get('model_name')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "User with the provided username does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            content_type = ContentType.objects.get(model=model_name)
        except ContentType.DoesNotExist:
            return Response({"message": f"Model '{model_name}' does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        permission_codename = f'can_change_{model_name}'
        try:
            permission = Permission.objects.get(codename=permission_codename)
        except Permission.DoesNotExist:
            return Response({"message": f"Permission '{permission_codename}' does not exist."},
                            status=status.HTTP_404_NOT_FOUND)

        # Assign the permission to the user
        user.user_permissions.add(permission)

        return Response({"message": f"Permission assigned to user: {username} for model: {model_name}"},
                        status=status.HTTP_200_OK)

