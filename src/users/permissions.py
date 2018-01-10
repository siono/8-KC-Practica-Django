from rest_framework.permissions import BasePermission


class UsersPermission(BasePermission):

    # Listado de usuarios: solo lo puede ver un usuario administrador (y por lo tanto autenticado)
    # Creación de usuarios: cualquier usuario
    # Detalle de usuario: los admin puede ver cualquier usuario, usuarios autenticados (no admin) pueden ver sus datos, no autenticados no pueden ver nada
    # Actualización de usuario:  los admin puede ver cualquier usuario, usuarios autenticados (no admin) pueden ver sus datos, no autenticados no pueden ver nada
    # Borrado de usuario:  los admin puede ver cualquier usuario, usuarios autenticados (no admin) pueden ver sus datos, no autenticados no pueden ver nada

    def has_permission(self, request, view):
        """
        Define si el usuario puede ejecutar una acción (GET, POST, PUT o DELETE) sobre la vista 'view'
        """

        from users.api import UserDetailAPI #para eliminar la dependeica circular entre users/api y users/permission

        if request.method == "POST" or request.user.is_superuser:
            return True

        if request.user.is_authenticated and request.method == "GET" and  isinstance(view, UserDetailAPI):
            return True

        return request.user.is_authenticated and (request.method == "PUT" or request.method == "DELETE")

    def has_object_permission(self, request, view, obj):
        """
        El usuario autenticado (request.user) solo puede trabajar con el usuario solicitado (obj) si es el mismo o un administrador
        """
        return request.user == obj or request.user.is_superuser