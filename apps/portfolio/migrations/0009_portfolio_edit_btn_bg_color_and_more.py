# Generated by Django 5.1.3 on 2024-11-24 15:55

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_portfolio_left_column_bg_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='edit_btn_bg_color',
            field=colorfield.fields.ColorField(default='#0d209c', image_field=None, max_length=25, samples=None, verbose_name='Edit button background color'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='edit_btn_svg_color',
            field=colorfield.fields.ColorField(default='#ffffff', image_field=None, max_length=25, samples=None, verbose_name='Edit button SVG color'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='pdf_btn_bg_color',
            field=colorfield.fields.ColorField(default='#9c0d0d', image_field=None, max_length=25, samples=None, verbose_name='PDF button background color'),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='pdf_btn_svg_color',
            field=colorfield.fields.ColorField(default='#ffffff', image_field=None, max_length=25, samples=None, verbose_name='PDF button SVG color'),
        ),
    ]
