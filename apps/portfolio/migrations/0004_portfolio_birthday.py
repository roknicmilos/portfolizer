# Generated by Django 5.1.2 on 2024-11-21 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_alter_portfolio_address_label_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='birthday'),
        ),
    ]