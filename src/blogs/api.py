from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from blogs.models import Blog
from blogs.serializers import BlogsListSerializer


class BlogsListAPI(ListAPIView):

    queryset = Blog.objects.all()
    serializer_class = BlogsListSerializer

    # para habilitar la busqueda, ordenación
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name","user__username"]
    ordering_fields = ["name","user__username"]
