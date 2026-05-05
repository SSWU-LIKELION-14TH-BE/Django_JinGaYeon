from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view,mypage_view, edit_profile_view, home_view, find_password_view, reset_password_view


urlpatterns = [
    path('signup/', signup_view, name='signup'),    #함수뷰
    path('home/', home_view, name='home'),

    path('login/', auth_views.LoginView.as_view(    #클래스뷰
        template_name='registration/login.html'
    ), name='login'),

    path('Find_pw/', find_password_view, name='find_password'),
    path('Reset_pw/', reset_password_view, name='reset_password'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('mypage/', mypage_view, name='mypage'),
    path('edit/', edit_profile_view, name='edit_profile'),
]