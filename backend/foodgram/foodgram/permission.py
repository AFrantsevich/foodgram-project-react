from rest_framework import permissions


class IsAuthenticatedOrReadOnlyIsAuthorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif (request.method == 'POST' or request.method == 'PATCH'
              or request.method == 'DELETE'):
            return request.user.is_authenticated or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.method == 'PATCH' or request.method == 'DELETE':
            return obj.author == request.user or request.user.is_staff
