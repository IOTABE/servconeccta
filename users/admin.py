from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ProfessionalProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_verified', 'is_active']
    list_filter = ['user_type', 'is_verified', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('user_type', 'phone', 'whatsapp', 'avatar', 'is_verified', 'is_active_whatsapp')}),
    )


@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'state', 'status', 'rating', 'total_jobs']
    list_filter = ['status', 'city', 'state', 'is_individual']
    search_fields = ['user__username', 'user__email', 'bio', 'cnpj', 'cpf']
    raw_id_fields = ['user']
    readonly_fields = ['rating', 'total_reviews', 'total_jobs']