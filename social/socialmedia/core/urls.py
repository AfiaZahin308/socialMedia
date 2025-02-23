from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
]