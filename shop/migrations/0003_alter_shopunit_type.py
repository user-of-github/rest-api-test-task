# Generated by Django 4.0.5 on 2022-06-19 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_shopunit_delete_shopunittype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopunit',
            name='type',
            field=models.CharField(choices=[('CATEGORY', 'CATEGORY'), ('OFFER', 'OFFER')], max_length=100),
        ),
    ]
