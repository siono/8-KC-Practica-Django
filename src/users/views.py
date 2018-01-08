from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import RedirectView

from users.forms import LoginForm
from django.contrib.auth import authenticate,login as django_login, logout as django_logout

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