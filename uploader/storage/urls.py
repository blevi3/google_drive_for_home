from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView
urlpatterns = [
    path('home', views.upload, name='upload'),
    path('download/<int:id>/', views.download, name='download'),
    path('share/<int:id>/', views.share, name='share'),
    path('shared_with_you/', views.shared_with_you, name='shared_with_you'),
    path('remove/<int:id>/', views.delete_object, name='remove'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('enter_otp/<int:user_id>/', views.enter_otp_view, name='enter_otp'),

]
