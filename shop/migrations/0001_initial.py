# Generated by Django 4.0.5 on 2022-06-18 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopUnitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(choices=[('OFFER', 'OFFER'), ('CATEGORY', 'CATEGORY')], default='OFFER', max_length=15, unique=True)),
            ],
        ),
    ]