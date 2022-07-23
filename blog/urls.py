from django.urls import path
from blog import views

urlpatterns = [
 path("accounts/signup", views.SignUpView.as_view(), name="signup"),
 path("accounts/login", views.LoginView.as_view(), name="login"),
 path("home", views.IndexView.as_view(), name="home"),
 path("users/profile/add", views.CreateUserProfileView.as_view(), name="add-profile"),
 path("users/profiles", views.ViewMyprofileView.as_view(), name="view-my-profile"),
 path("users/password/change", views.PasswordResetView.as_view(), name="password-reset"),
 path("users/profile/change/<int:user_id>", views.ProfileUpdateView.as_view(), name="profile-update"),
 path("users/profile_pic/change/<int:user_id>", views.ProfilePicUpdateView.as_view(), name="update-profile"),
 path("post/comment/<int:post_id>", views.add_comment, name="add-comment"),
 path("post/like/add/<int:post_id>", views.add_like, name="add-like")

]
