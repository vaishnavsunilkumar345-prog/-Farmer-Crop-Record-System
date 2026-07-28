from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('crops/add/', views.add_crop, name='add_crop'),
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/edit/<int:pk>/', views.edit_crop, name='edit_crop'),
    path('crops/delete/<int:pk>/', views.delete_crop, name='delete_crop'),
]
