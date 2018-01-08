from datetime import datetime

from django.shortcuts import render
from django.views import View

from blogs.models import Post, Blog
from wordplease.settings import POSTS_TO_SHOW


class PostQuerySet(object):

    def get_public_post(self):
        return Post.objects.filter(publication_date__lte=datetime.now()).order_by("-publication_date")


class PostList(PostQuerySet,View):

    def get(self, request):
        latest_posts = super(PostList,self).get_public_post()[:POSTS_TO_SHOW]
        context = {'posts': latest_posts}
        return render(request, "home.html", context)


class BlogList(View):

    def get(self, request):
        list_blogs = Blog.objects.all()
        context = { 'blogs': list_blogs}
        return render(request, "blog_list.html", context)


class BlogDetail(PostQuerySet,View):

    def get(self,request,user):
        posts_blog = super(BlogDetail,self).get_public_post().filter(blog__user__username = user)
        if len(posts_blog) == 0:
            return render(request, "404.html", status=404)
        else:
            context = { 'posts': posts_blog, 'user': user}
            return render(request,"blog_detail.html",context)

class PostDetail(View):

    def get(self,request,user,pk):
        post_detail = Post.objects.filter(blog__user__username = user).filter(pk=pk)
        if len(post_detail) == 0:
            return render(request, "404.html", status=404)
        else:
            context = {'post': post_detail[0]}
            return render(request, "post_detail.html", context)

