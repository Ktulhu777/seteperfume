# Generated by Django 5.0.2 on 2024-03-10 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('men', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='product_review',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='men.perfume'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review',
            field=models.TextField(blank=True, null=True, verbose_name='Отзыв'),
        ),
    ]
