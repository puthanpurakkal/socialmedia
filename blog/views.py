from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from blog.forms import UserRegistrationForm, LoginForm
from django.views.generic import View, CreateView, FormView, TemplateView
from django.contrib.auth import authenticate, login, logout
# Create your views here.

class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    model = User
    success_url = reverse_lazy("signin")

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request, self.template_name, {"form": form})
    # def post(self,request,*args,**kwargs):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("")
    #     else:
    #         return render(request, self.template_name, {"form": form})


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    model = User


    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #
    #     return render(request,self.template_name, {"form": form})
    #
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                print("success")
                login(request, user)
            return redirect("home")
        else:
            return render(request, self.template_name, {"form": form})


class IndexView(TemplateView):
    template_name = "home.html"
    # def get(self,request,*args,**kwargs):
    #     return render(request, self.template_name)
