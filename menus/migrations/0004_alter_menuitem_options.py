# Generated by Django 4.2 on 2023-05-05 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_remove_menuitem_named_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'verbose_name': 'Меню', 'verbose_name_plural': 'Меню'},
        ),
    ]
