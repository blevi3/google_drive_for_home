from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path('home', views.upload, name='upload'),
    path('download/<int:id>/', views.download, name='download'),
    path('share/<int:id>/', views.share, name='share'),
    path('shared_with_you/', views.shared_with_you, name='shared_with_you'),
    path('remove/<int:id>/', views.delete_object, name='remove'),


]
