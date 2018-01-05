from datetime import datetime

from django.db.models import Prefetch
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

    def get(self,request,slug):
        posts_blog = super(BlogDetail,self).get_public_post().filter(blog__name = slug)
        context = { 'posts': posts_blog}
        return render(request,"blog_detail.html",context)
