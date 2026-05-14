from django.db import models
from django.conf import settings


class ServiceCategory(models.Model):
    """Categorias de serviços com imagem para definição visual"""

    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    is_active = models.BooleanField(default=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_categories'
        verbose_name = 'Categoria de Serviço'
        verbose_name_plural = 'Categorias de Serviços'
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'parent']),
        ]

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    """Solicitação de serviço por cliente"""

    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('quoted', 'Orçamento Enviado'),
        ('accepted', 'Aceito'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='service_requests'
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name='requests',
        null=True,
        blank=True
    )

    is_custom = models.BooleanField(
        default=False,
        help_text="Indica se é uma solicitação fora do catálogo"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True
    )
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True, db_index=True)
    state = models.CharField(max_length=2, blank=True, db_index=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )

    budget_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    budget_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    images = models.ManyToManyField(
        'ServiceImage',
        blank=True,
        related_name='requests'
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'service_requests'
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['city', 'state']),
            models.Index(fields=['client', 'status']),
        ]

    def __str__(self):
        return f"{self.title} - {self.client.username}"


class ServiceImage(models.Model):
    """Imagens de solicitações de serviço"""

    image = models.ImageField(upload_to='service_requests/')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'service_images'


class ProfessionalService(models.Model):
    """Serviços oferecidos por profissional"""

    professional = models.ForeignKey(
        'users.ProfessionalProfile',
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name='professional_services'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price_type = models.CharField(
        max_length=20,
        choices=[
            ('fixed', 'Fixo'),
            ('hourly', 'Por Hora'),
            ('negotiable', 'Negociável'),
        ],
        default='fixed'
    )
    is_active = models.BooleanField(default=True, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'professional_services'
        unique_together = ['professional', 'category']
        indexes = [
            models.Index(fields=['is_active', 'professional']),
        ]

    def __str__(self):
        return f"{self.title} - {self.professional.user.get_full_name()}"