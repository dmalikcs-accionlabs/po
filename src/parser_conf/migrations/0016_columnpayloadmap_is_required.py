# Generated by Django 2.2.4 on 2019-09-16 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parser_conf', '0015_auto_20190910_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='columnpayloadmap',
            name='is_required',
            field=models.BooleanField(default=False),
        ),
    ]