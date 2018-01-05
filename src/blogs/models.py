from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Devuelve la representación de un objeto como un string

        """
        return self.name

class Blog(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, related_name="blog",on_delete=models.CASCADE) #one user only have one blog
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """
        Devuelve la representación de un objeto como un string

        """
        return self.name

class Post(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE) #on_delete=models.CASCADE = Si se borra el usuario se borra todas las post que haya realizado.

    title = models.CharField(max_length=150)
    summary = models.TextField(max_length=500)
    body = models.TextField()
    multimedia = models.URLField(blank=True, null=True)
    publication_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)  # saves the date when the object is created
    modified_at = models.DateTimeField(auto_now_add=True)  # saves the date when the object is update

    category = models.ManyToManyField(Category)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):

        return self.title
