# Generated by Django 4.2 on 2023-04-30 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='is_root',
            field=models.BooleanField(default=False),
        ),
    ]
