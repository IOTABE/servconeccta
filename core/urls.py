from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar/', views.search, name='search'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('servico-personalizado/', views.custom_service_view, name='custom_service'),
]
