from django.urls import path
from .views import post_list, post_like, post_create, post_detail, post_update, post_delete
from .views import comment,comment_reply, comment_create, comment_delete,comment_like
urlpatterns = [
    path('', post_list, name='post_list'),
    path('create/', post_create, name='post_create'),
    path('<int:pk>/', post_detail, name='post_detail'),
    path('<int:pk>/comment/', comment, name='comment'),
    path('<int:pk>/comment/create/', comment_create, name='comment_create'),
    path('<int:pk>/<int:comment_pk>/delete/', comment_delete, name='comment_delete'),
    path('<int:pk>/update/', post_update, name='post_update'),
    path('<int:pk>/delete/', post_delete, name='post_delete'),
    path('<int:pk>/like/', post_like, name='post_like'),
    path('<int:pk>/comment/<int:comment_pk>/like/', comment_like, name='comment_like'),
    path('<int:pk>/comment/<int:comment_pk>/reply/', comment_reply, name='comment_reply')
]