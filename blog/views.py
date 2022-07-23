from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from blog.forms import UserRegistrationForm, LoginForm, UserProfileForm, PasswordResetForm, ProfilePicUpdateForm, BlogForm, CommentForm
from django.views.generic import View, CreateView, FormView, TemplateView, UpdateView
from blog.models import UserProfile, Blogs, Comments
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator

# Create your views here.

def signinrqd(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return fn(request, *args, **kwargs)
        else:
            messages.error(request, "You must login")
            return redirect("signin")
    return wrapper

class SignUpView(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    model = User
    success_url = reverse_lazy("login")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})
    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("")
        else:
            return render(request, self.template_name, {"form": form})



class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"
    model = User

    # @signinrqd
    # def sign_out(request, *args, **kwargs):
    #     logout(request)
    #     return redirect("sign-in")

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     return render(request,self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
        if user:
            print("success")
            login(request, user)
            messages.success(self.request, "profile has been created")
            return redirect("home")
        else:
            messages.error(request, "password incorrect")
            return render(request, self.template_name, {"form": form})

# @signinrqd
# def log_out(request, *args, **kwargs):
#     logout(request)
#     return redirect("signin")

class IndexView(CreateView):
    model = Blogs
    form_class = BlogForm
    success_url = reverse_lazy("home")
    template_name = "home.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        self.object = form.save()
        messages.success(self.request, "post has been saved!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blogs.objects.all().order_by("-posted_date")
        context["blogs"] = blogs
        comment_form = CommentForm()
        context["comment_form"] = comment_form
        return context

class CreateUserProfileView(CreateView):
    model = UserProfile
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     self.object = form.save()
    #     messages.success(self.request,"profile has been created")
    #     return redirect("home")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(self.request, "profile has been created")
            return redirect("home")
        else:
            return render(request, self.template_name, {"form": form})

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "profile has been added")
        self.object = form.save()
        return super().form_valid(form)


class ViewMyprofileView(TemplateView):
    template_name = "view-profile.html"

class PasswordResetView(FormView):
    template_name = "passwodreset.html"
    form_class = PasswordResetForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            oldpassword = form.cleaned_data.get("old_password")
            password1 = form.cleaned_data.get("new_password")
            password2 = form.cleaned_data.get("confirm_password")
            user = authenticate(request, username=request.user.username, password=oldpassword)
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request, "password changed successfully")
                return redirect("login")
            else:
                messages.error(request, "invalid credentials")
                return render(request, self.template_name, {"form": form})

class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"
    def form_valid(self, form):
        messages.success(self.request, "your profile has been successfully updated!")
        self.object = form.save()
        return super().form_valid(form)

class ProfilePicUpdateView(UpdateView):
    form_class = ProfilePicUpdateForm
    template_name = "update-profile.html"
    model = UserProfile
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"
    def form_valid(self, form):
        messages.success(self.request, "profile pic has been updated")
        self.object = form.save()
        return super().form_valid(form)

def add_comment(request,*args,**kwargs):
    if request.method == 'POST':
        blog_id = kwargs.get("post_id")
        blog = Blogs.objects.get(id=blog_id)
        user = request.user
        comment = request.POST.get('comment')
        Comments.objects.create(blog=blog, user=user, comment=comment)
        messages.success(request, "comment added")
        return redirect("home")

def add_like(request,*args,**kwargs):
    blog_id = kwargs.get("post_id")
    blog = Blogs.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    messages.success(request, "like added")
    return redirect("home")
