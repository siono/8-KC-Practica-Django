from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from blogs.form import PostForm
from blogs.models import Post, Blog
from wordplease.settings import POSTS_TO_SHOW


class PostQuerySet(object):

    def get_public_post(self):
        return Post.objects.filter(publication_date__lte=datetime.now()).order_by("-publication_date")


class PostList(PostQuerySet,View):

    def get(self, request):
        post_list = super(PostList,self).get_public_post()
        paginator = Paginator(post_list, POSTS_TO_SHOW)
        page = request.GET.get('page')
        posts = paginator.get_page(page)
        context = {'posts': posts, 'title_page': 'Wellcome to WordPlease'}
        return render(request, "post_list.html", context)


class BlogList(View):

    def get(self, request):
        list_blogs = Blog.objects.all()
        context = { 'blogs': list_blogs}
        return render(request, "blog_list.html", context)


class BlogDetail(PostQuerySet,View):

    def get(self,request,user):
        posts_blog = super(BlogDetail,self).get_public_post().filter(blog__user__username = user)
        if len(posts_blog) == 0:
            context = {'message': "No existen post publicados"}
            return render(request, "404.html",context, status=404)
        else:
            context = { 'posts': posts_blog, 'user': user, 'title_page': user + ' blog'}
            return render(request,"post_list.html",context)

class PostDetail(View):

    def get(self,request,user,pk):
        post_detail = Post.objects.filter(blog__user__username = user).filter(pk=pk)
        if len(post_detail) == 0:
            context = {'message': "Post no encontrado o eliminado"}
            return render(request, "404.html", context, status=404)
        else:
            context = {'post': post_detail[0]}
            return render(request, "post_detail.html", context)


class CreatePost(LoginRequiredMixin,View):

    def get(self, request):
        form = PostForm()
        return render(request, "post_form.html", {'form': form})

    def post(self, request):
        post = Post()
        post.user = request.user
        post.blog = request.user.blog
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            #vaciamos el formulario
            form = PostForm()
            url = reverse("post_detail", args=[post.user,post.pk]) #reverse genera url pasandole el tipo de URL
            message = " created successfully!"
            message += '<a href="{0}">Create your first post</a>'.format(url)
            #enviamos mensaje de exito con un enlace a la pelicula que acabamos de cr
            messages.success(request, message)
        return render(request, "post_form.html", {'form':form})


