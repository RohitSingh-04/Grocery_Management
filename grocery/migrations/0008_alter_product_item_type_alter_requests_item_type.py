# Generated by Django 5.0.1 on 2024-07-14 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grocery', '0007_remove_requests_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='grocery.type'),
        ),
        migrations.AlterField(
            model_name='requests',
            name='item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='grocery.type'),
        ),
    ]