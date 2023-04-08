from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        if (request.user and request.user.is_authenticated) and request.user.groups.filter(name='Автор').exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.has_perms([
            'learning.add_course', 'learning.change_course', 'learning.delete_course'
        ]):
            return True
        return False
