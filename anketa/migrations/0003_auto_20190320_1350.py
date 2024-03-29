# Generated by Django 2.1.2 on 2019-03-20 10:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('anketa', '0002_partner_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'verbose_name': 'Организация', 'verbose_name_plural': 'Организации'},
        ),
        migrations.AlterModelOptions(
            name='partner',
            options={'verbose_name': 'Партнер', 'verbose_name_plural': 'Партнеры'},
        ),
        migrations.AddField(
            model_name='organization',
            name='customer',
            field=models.ManyToManyField(related_name='organization_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='customer',
            field=models.ManyToManyField(related_name='partner_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
    ]
