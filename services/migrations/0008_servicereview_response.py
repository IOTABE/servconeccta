from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_servicerequest_professional_and_service_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicereview',
            name='response',
            field=models.TextField(blank=True, help_text='Resposta do profissional à avaliação'),
        ),
        migrations.AddField(
            model_name='servicereview',
            name='response_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]