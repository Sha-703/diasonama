from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncadreurAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervised_encadreurs', to=settings.AUTH_USER_MODEL)),
                ('encadreur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_supervisors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('supervisor', 'encadreur')},
            },
        ),
    ]
