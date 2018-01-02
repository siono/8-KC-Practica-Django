from datetime import datetime

from django.shortcuts import render

from blogs.models import Post


def home(request):
    latest_posts = Post.objects.filter(publication_date__lte = datetime.now()).order_by("-publication_date")

    context = {'posts': latest_posts}
    return render(request, "home.html",context)
