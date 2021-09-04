from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.loginpage, name = "Loginpage"),
    path ('gsignin/', views.GoogleSignin, name = "Gsign"),
    path ('home', views.firebaseLoginAuth, name = "Dashboard"),  
    path ('Signup', views.signup, name = "Signup"),  
    path ('PostSignup', views.postsignup, name  = "Postsignup"),
    path ('Upload', views.uploadfile, name  = "uploadfile"),
    path ('logout', views.logout, name = "logout"),
    path ('collab', views.invite, name = "invite"),
    ]