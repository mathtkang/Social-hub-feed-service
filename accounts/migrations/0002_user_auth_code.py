# Generated by Django 4.2.6 on 2023-10-27 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
