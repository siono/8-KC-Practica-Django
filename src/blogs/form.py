from django.forms import ModelForm

from blogs.models import Post


class PostForm(ModelForm):
    class Meta:
            model = Post
            fields = '__all__'
            exclude = ["user","blog"] #exclude el campo user y blog en el formulario
