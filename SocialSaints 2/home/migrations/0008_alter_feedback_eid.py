# Generated by Django 3.2.18 on 2023-04-09 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_volunteers'),
        ('home', '0007_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='eid',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='event.event'),
        ),
    ]
