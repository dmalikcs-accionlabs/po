# Generated by Django 2.2.4 on 2019-08-25 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0008_auto_20190825_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingestiondata',
            name='status',
            field=models.CharField(choices=[('N', 'NEW'), ('C_F', 'Failed'), ('C_S', 'Completed')], default='N', max_length=5),
        ),
    ]