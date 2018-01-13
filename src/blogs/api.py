from datetime import datetime
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blogs.models import Blog, Post
from blogs.permissions import PostPermission
from blogs.serializers import BlogsListSerializer, PostListSerializer, PostDetailSerializer
from users.permissions import UsersPermission


class BlogsListAPI(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogsListSerializer

    # para habilitar la busqueda, ordenación
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "user__username"]
    ordering_fields = ["name", "user__username"]


class PostListAPI(ListCreateAPIView):
    queryset = Post.objects.select_related('blog__user').order_by('-publication_date')
    permission_classes = [IsAuthenticatedOrReadOnly]

    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "summary"]
    ordering_fields = ["title", "publication_date"]

    def get_queryset(self):

        # si no está autenticado -> post publicados
        if not self.request.user.is_authenticated:
            return self.queryset.all().filter(publication_date__lte=datetime.now())

        # usuario administrador -> todos los post
        elif self.request.user.is_superuser:
            return self.queryset.all()

        # si no es un administrador pero esta logueado -> sus post
        else:
            return self.queryset.filter(blog=self.request.user.blog)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, blog=self.request.user.blog)


class PostDetailAPI(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('blog__user').order_by('-publication_date')
    serializer_class = PostDetailSerializer
    permission_classes = [PostPermission]

    # para que un usuario no pueda actualizar o borrar peliculas de otro usuario
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
