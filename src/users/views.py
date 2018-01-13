from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import RedirectView
from django.contrib.auth.models import User

from blogs.models import Blog
from users.forms import LoginForm, UserForm
from django.contrib.auth import authenticate, login as django_login, logout as django_logout, update_session_auth_hash


class LoginView(View):

    def get(self,request):
        context = {'form': LoginForm()}
        return render(request, "login_form.html", context)

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("login_username")
            password = form.cleaned_data.get("login_password")
            authenticate_user = authenticate(username=username, password=password)
            if authenticate_user and authenticate_user.is_active:
                django_login(request, authenticate_user)
                redirect_to = request.GET.get("next", "home_page") # si no existe el parametro next devolvemos el segundo parametro en este caso home_page
                return redirect(redirect_to)
            else:
                messages.error(request, "Usuario incorrecto o inactivo")
        return render(request, "login_form.html", {'form': form})


class LogoutView(RedirectView):

    def get(self,request):
        django_logout(request)
        return redirect("home_page")


class SingupView(View):

     def get(self,request):
         context = {'form': UserForm()}
         return render(request, "singup_form.html", context)

     def post(self,request):
         user = User()
         form = UserForm(data=request.POST)
         form.instance = user
         if form.is_valid():

             user.first_name = form.cleaned_data.get('first_name')
             user.last_name = form.cleaned_data.get('last_name')
             user.email = form.cleaned_data.get('email')
             user.username = form.cleaned_data.get('username')
             password = form.cleaned_data.get('password')
             user.set_password(password)
             user.save()

             blog = Blog(user=user)
             blog.name = form.cleaned_data.get('blog_name')
             blog.description = form.cleaned_data.get('blog_description')
             blog.save()

             # logeamos al usaurio
             authenticate_user = authenticate(username=user.username, password=password)
             django_login(request, authenticate_user)

             # vaciamos el formulario
             form = UserForm()
             url = reverse("create_post")
             message = "User with blog created successfully!"
             message += '<a href="{0}">Create you first post</a>'.format(url)
             # enviamos mensaje de exito con un enlace al blog que acabamos de crear
             messages.success(request, message)

         return render(request, "singup_form.html", {'form': form})


