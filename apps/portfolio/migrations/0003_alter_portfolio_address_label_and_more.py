# Generated by Django 5.1.2 on 2024-10-20 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfolio',
            name='address_label',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='address label'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='address_link',
            field=models.URLField(blank=True, max_length=1000, null=True, verbose_name='address link'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='role'),
        ),
    ]