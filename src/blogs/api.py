from datetime import datetime
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from blogs.models import Blog, Post
from blogs.serializers import BlogsListSerializer, PostListSerializer
from blogs.views import PostList


class BlogsListAPI(ListAPIView):

    queryset = Blog.objects.all()
    serializer_class = BlogsListSerializer

    # para habilitar la busqueda, ordenación
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name","user__username"]
    ordering_fields = ["name","user__username"]

class PostListAPI(ListAPIView):

    queryset = Post.objects.select_related('blog__user').order_by('-publication_date')

    serializer_class = PostListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["title", "summary"]
    ordering_fields = ["title", "publication_date"]

    def get_queryset(self):
        """
        If user is not authenticated, returns only published posts
        If user is authenticated and not superuser, returns all its posts and published posts from others
        If user is superuser, returns all posts
        """

        # si no está autenticado -> post publicados
        if not self.request.user.is_authenticated:
            return self.queryset.all().filter(publication_date__lte=datetime.now())

        # usuario administrador -> todos los post
        elif self.request.user.is_superuser:
            return self.queryset.all()

        # si no es un administrador pero esta logueado -> sus post
        else:
            return self.queryset.filter(blog=self.request.user.blog)



