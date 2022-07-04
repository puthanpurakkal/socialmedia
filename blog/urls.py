from django.urls import path
from blog import views

urlpatterns = [
 path("accounts/signup", views.SignUpView.as_view(), name="signup"),
 path("accounts/signin", views.LoginView.as_view(), name="signin"),
 path("home", views.IndexView.as_view(), name="home")
]
