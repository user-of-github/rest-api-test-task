# Generated by Django 4.0.5 on 2022-06-20 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_shopunit_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopunit',
            name='total_inner_sum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shopunit',
            name='totally_inner_goods_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='shopunit',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]