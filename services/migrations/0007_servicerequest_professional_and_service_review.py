from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_servicerequest_service_type'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='professional',
            field=models.ForeignKey(
                blank=True,
                help_text='Profissional que aceitou/realiza o serviço',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='service_jobs',
                to='users.professionalprofile'
            ),
        ),
        migrations.CreateModel(
            name='ServiceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(choices=[(1, '1 - Ruim'), (2, '2 - Regular'), (3, '3 - Bom'), (4, '4 - Muito Bom'), (5, '5 - Excelente')])),
                ('title', models.CharField(blank=True, max_length=100)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('professional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_received', to='users.professionalprofile')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_given', to='users.user')),
                ('service_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='services.servicerequest')),
            ],
            options={
                'db_table': 'service_reviews',
                'unique_together': {('service_request', 'reviewer')},
            },
        ),
        migrations.AddIndex(
            model_name='servicereview',
            index=models.Index(fields=['professional', 'created_at'], name='service_rev_profess_idx'),
        ),
        migrations.AddIndex(
            model_name='servicereview',
            index=models.Index(fields=['rating'], name='service_rev_rating_idx'),
        ),
    ]