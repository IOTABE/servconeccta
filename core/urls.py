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
    path('editar-perfil/', views.edit_profile_view, name='edit_profile'),
    path('encerrar-servico/<int:service_id>/', views.complete_service_view, name='complete_service'),
    path('meus-servicos/', views.my_services_view, name='my_services'),
]
