from django.forms import ModelForm, forms
from django.forms.widgets import Input

from blogs.models import Post


class PostForm(ModelForm):
    error_css_class = "error"

    class Meta:
            model = Post
            fields = '__all__'
            exclude = ["user","blog"] #exclude el campo user y blog en el formulario


    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'