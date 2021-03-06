# Generated by Django 2.2.4 on 2019-08-30 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('ingestion', '0011_auto_20190829_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingestiondata',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='ingestiondata',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
