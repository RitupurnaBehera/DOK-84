from rest_framework.permissions import BasePermission

class CanChangeBookshopPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_bookshop' permission
        return request.user.has_perm('accounts.can_change_bookshop')

class CanChangeRestaurantsPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_bookshop' permission
        return request.user.has_perm('accounts.can_change_restaurants')

class CanChangeClinicsPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_bookshop' permission
        return request.user.has_perm('accounts.can_change_clinics')

class CanChangePetshopPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'can_change_bookshop' permission
        return request.user.has_perm('accounts.can_change_petshop')

