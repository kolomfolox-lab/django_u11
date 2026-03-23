from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('<int:id>/edit/', views.post_edit, name='post_edit'),
    path('<int:id>/delete/', views.post_delete, name='post_delete'),
]
