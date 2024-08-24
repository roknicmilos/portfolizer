# Generated by Django 5.1 on 2024-08-18 20:09

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='slug')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('filename', models.CharField(max_length=100, verbose_name='filename')),
                ('avatar', models.ImageField(null=True, upload_to='cv/img/', verbose_name='avatar')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('role', models.CharField(max_length=100, verbose_name='role')),
                ('email', models.EmailField(max_length=100, verbose_name='email')),
                ('phone', models.CharField(max_length=20, verbose_name='phone')),
                ('address_label', models.CharField(max_length=100, verbose_name='address label')),
                ('address_link', models.URLField(max_length=1000, verbose_name='address link')),
                ('about_me', models.TextField(verbose_name='about me')),
            ],
            options={
                'verbose_name': 'CV',
                'verbose_name_plural': 'CVs',
            },
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('company', models.CharField(max_length=100, verbose_name='company')),
                ('start', models.DateField(help_text="Day is not important. Select 1st if you don't know the exact start day.", verbose_name='start')),
                ('end', models.DateField(blank=True, help_text="Leave empty if you are currently working here. Day is not important. Select 1st if you don't know the exact end day.", null=True, verbose_name='end')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('description', models.TextField(verbose_name='description')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employments', to='cv.cv', verbose_name='CV')),
            ],
            options={
                'verbose_name': 'Employment',
                'verbose_name_plural': 'Employments',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('linkedin', 'LinkedIn'), ('github', 'GitHub')], max_length=10, verbose_name='type')),
                ('label', models.CharField(max_length=100, verbose_name='label')),
                ('url', models.URLField(verbose_name='URL')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='cv.cv', verbose_name='CV')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'Links',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100, verbose_name='label')),
                ('level', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='level')),
                ('cv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skills', to='cv.cv', verbose_name='cv')),
            ],
            options={
                'verbose_name': 'skill',
                'verbose_name_plural': 'skills',
            },
        ),
    ]