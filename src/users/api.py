from django.contrib.auth.models import User
from rest_framework.generics import get_object_or_404
from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import UsersPermission
from users.serializers import UserSerializer


class UsersListAPI(APIView):

    permission_classes = [UsersPermission]

    def get(self,request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['is_active'] = True #activamos por defecto al usuario creado
            user = serializer.save()#llamo a la funcion del serializer del Usuario
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPI(APIView):

    permission_classes = [UsersPermission]

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request,user) #como hemos implementado manualmente los metodos tenemos que checkear los metodos de forma manual tambien
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = UserSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)