from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer



class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password1 = request.data.get('password1')
        

        if not username or not password1:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            user = User.objects.get(username=username, password1=password1)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)




class UserRegistrationView(APIView):
    def get(self, request):
        queryset = User.objects.get(id=request.data.get('id'))
        serializer = UserSerializer(queryset)
        return Response(serializer.data)

    def post(self, request):

        password1 = request.data.get('password1')
        password2 = request.data.get('password2') 

        if not password1 or not password2:
            return Response({'message': 'Please provide password1, and password2'}, status=status.HTTP_400_BAD_REQUEST)

        if password1 != password2:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST) 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    


class AdminListView(APIView):

    

    def get(self,request):



        try:
            user_id = request.data.get('id')
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
        
        # try:
        #     user = User.objects.get(id = request.data.get('id'))
        #     user.role.name=="admin"
                
        # except:
        #     return Response({'message':"You don't have permission to perform actions"})
        
        # user = User.objects.all()
        # serializer = UserSerializer(user)
        # return Response(serializer.data)
        
    

# class UserDetailView(APIView):

    