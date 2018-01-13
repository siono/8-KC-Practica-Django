from rest_framework.permissions import BasePermission
from django.utils import timezone


class PostPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        """
            - Creación de Post: cualquier usuario autenticado
            - Modificación o Borrado: usuario propietario o administrador.
            - Detalle de Post: cualquier usuario verá los post publicos.
                               si no es publico: solo usuario propietario o administrador
        """
        if request.method == "POST":
            return request.user.is_authenticated

        if request.method == "PUT" or request.method == "DELETE":
            return request.user.is_superuser or request.user == obj.blog.user

        return request.method == "GET" and (request.user.is_superuser or request.user == obj.blog.user) or obj.publication_date <= timezone.now()
