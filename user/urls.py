from django.urls import path
from django.contrib.auth import views as auth_views
from .views import signup_view,mypage_view, guestbook_create_view, guestbook_delete_view
from .views import edit_profile_view, home_view, user_guestbook_view, my_guestbook_view ,find_password_view, reset_password_view


urlpatterns = [
    path('signup/', signup_view, name='signup'),    #함수뷰
    path('home/', home_view, name='home'),

    path('login/', auth_views.LoginView.as_view(    #클래스뷰
        template_name='registration/login.html'
    ), name='login'),

    path('Find_pw/', find_password_view, name='find_password'),
    path('Reset_pw/', reset_password_view, name='reset_password'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('mypage/', mypage_view, name='mypage'), #마이페이지
    path('edit/', edit_profile_view, name='edit_profile'),

     path('mypage/guestbook/', my_guestbook_view, name='my_guestbook'),
    path('users/<int:pk>/guestbook/', user_guestbook_view, name='user_guestbook'),
    path('users/<int:pk>/guestbook/create/', guestbook_create_view, name='guestbook_create'),
 
    path(
    'users/<int:pk>/guestbook/<int:guestbook_id>/delete/',guestbook_delete_view, name='guestbook_delete'),
]
