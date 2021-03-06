# Generated by Django 2.2.4 on 2019-08-26 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0009_auto_20190825_0950'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingestiondatatask',
            name='task',
            field=models.CharField(choices=[('ack', 'acknowledge'), ('validate_file_format', 'Validate file format task'), ('validate_column_name', 'Validate column names task'), ('validate_column_data', 'Validate column data task'), ('trans_data', 'Transformation data task'), ('prepare_payload_task', 'Prepare payload task'), ('send_payload_task', 'Send payload task'), ('handle_res_task', 'handle response task')], default='A', max_length=35),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingestiondatatask',
            name='status',
            field=models.CharField(choices=[('N', 'NEW'), ('C_F', 'Failed'), ('C_S', 'Completed')], max_length=35),
        ),
    ]
