"""
URL configuration for registration project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework_simplejwt.views import TokenRefreshView


from django.urls import path
from accounts.views import(UserRegistrationView,UserLoginView,AdminListView,SubuserOnlyAPIView,AdminDataAPIView,subuserregisterAPI,subuserloginAPI,BookshopAPIIView,RestaurantsAPIView,ClinicsAPIView,
PetsAPIView,AssignPermission)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',UserRegistrationView.as_view(),name = 'user-registration'),
    path('login/',UserLoginView.as_view(),name="user-login"),
    path('admin_users/',AdminListView.as_view(),name="admin_user_list"),
    path('subuser/',SubuserOnlyAPIView.as_view(),name="subuser-only-api"),
    path('admin-data/',AdminDataAPIView.as_view(),name="admin-data"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('subuser-register/',subuserregisterAPI.as_view(),name = "subuser-register"),
    path('subuserlogin/',subuserloginAPI.as_view(), name="subuser-login"),
    
    path('book/',BookshopAPIIView.as_view(), name="bookshop"),
    path('restaurants/',RestaurantsAPIView.as_view(), name="restaurants"),
    path('clinics/',ClinicsAPIView.as_view(), name="clinics"),
    path('pets/',PetsAPIView.as_view(), name="pets"),
    path('assign_permission/', AssignPermission.as_view(), name='assign-permission'),

    
]
