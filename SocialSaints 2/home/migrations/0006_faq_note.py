# Generated by Django 3.0.7 on 2023-03-28 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_faq_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='note',
            field=models.BooleanField(default=False),
        ),
    ]
