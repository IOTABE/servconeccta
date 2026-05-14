from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuario customizado com campos extras para a plataforma"""

    USER_TYPE_CHOICES = [
        ('client', 'Cliente'),
        ('professional', 'Profissional'),
        ('admin', 'Administrador'),
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='client',
        db_index=True
    )
    phone = models.CharField(max_length=20, blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active_whatsapp = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['user_type', 'is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.get_full_name() or self.username


class ProfessionalProfile(models.Model):
    """Perfil profissional com dados de geolocalização para buscas"""

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('suspended', 'Suspenso'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='professional_profile'
    )
    bio = models.TextField(blank=True)
    cpf = models.CharField(max_length=14, blank=True)
    cnpj = models.CharField(max_length=18, blank=True)
    is_individual = models.BooleanField(default=True)

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        db_index=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        db_index=True
    )
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True, db_index=True)
    state = models.CharField(max_length=2, blank=True, db_index=True)
    postal_code = models.CharField(max_length=10, blank=True)

    radius_service_km = models.PositiveIntegerField(default=10)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )
    total_reviews = models.PositiveIntegerField(default=0)
    total_jobs = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'professional_profiles'
        indexes = [
            models.Index(fields=['status', 'user']),
            models.Index(fields=['city', 'state']),
            models.Index(fields=['latitude', 'longitude']),
        ]

    def __str__(self):
        return f"Prof: {self.user.get_full_name()}"