# Generated by Django 2.2.4 on 2019-08-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='deleted_at',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='clientagent',
            name='deleted_at',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
