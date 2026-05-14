from django.contrib import admin
from .models import ServiceCategory, ServiceRequest, ServiceImage, ProfessionalService


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'category', 'city', 'state', 'status', 'budget_min', 'budget_max', 'created_at']
    list_filter = ['status', 'category', 'city', 'state', 'created_at']
    search_fields = ['title', 'description', 'client__username']
    raw_id_fields = ['client', 'category']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'uploaded_by', 'created_at']
    raw_id_fields = ['uploaded_by']


@admin.register(ProfessionalService)
class ProfessionalServiceAdmin(admin.ModelAdmin):
    list_display = ['professional', 'category', 'title', 'price', 'price_type', 'is_active']
    list_filter = ['is_active', 'price_type', 'category']
    search_fields = ['title', 'description']
    raw_id_fields = ['professional', 'category']