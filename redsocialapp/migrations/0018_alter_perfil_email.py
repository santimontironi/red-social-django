# Generated by Django 5.1.7 on 2025-04-05 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redsocialapp', '0017_alter_perfil_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
