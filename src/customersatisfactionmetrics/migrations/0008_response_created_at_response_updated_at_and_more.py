# Generated by Django 5.0.10 on 2025-01-10 11:40

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customersatisfactionmetrics', '0007_question_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='response',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
