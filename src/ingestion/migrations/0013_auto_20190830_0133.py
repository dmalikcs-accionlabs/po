# Generated by Django 2.2.4 on 2019-08-30 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0012_auto_20190830_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingestiondata',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='clients.ClientAgent'),
        ),
    ]
