# Generated by Django 3.2.18 on 2023-04-09 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('home', '0009_alter_feedback_eid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='uid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile'),
        ),
    ]