"""wordplease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from blogs.views import PostList, BlogList, BlogDetail, PostDetail, CreatePost
from users.api import UsersListAPI, UserDetailAPI
from users.views import LoginView, LogoutView,SingupView

urlpatterns = [
    path('', PostList.as_view(), name="home_page"),

    path('login/', LoginView.as_view(), name="user_login"),
    path('logout/', LogoutView.as_view(), name="user_logout"),
    path('signup/', SingupView.as_view(), name="user_singup"),

    path('new-post/', CreatePost.as_view(), name="create_post"),

    path('blogs/<str:user>/<int:pk>/', PostDetail.as_view(), name="post_detail"),
    path('blogs/<str:user>', BlogDetail.as_view(), name="blog_detail"),
    path('blogs/', BlogList.as_view(), name="blog_list"),

    path('admin/', admin.site.urls),

    # API REST
    path('api/1.0/users/', UsersListAPI.as_view(), name="api_users_list"),
    path('api/1.0/users/<int:pk>',UserDetailAPI.as_view(), name="api_user_detail")
]
