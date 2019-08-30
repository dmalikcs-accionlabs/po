# Generated by Django 2.2.4 on 2019-08-25 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parser_conf', '0002_auto_20190824_0825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='columnpayloadmap',
            name='config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='config_maps', to='parser_conf.ParserConfigurationDef'),
        ),
        migrations.AlterField(
            model_name='columnpayloadmap',
            name='payload',
            field=models.CharField(choices=[('venue', 'Venu'), ('eventdate', 'Event Date'), ('eventtime', 'Event Time'), ('event_name', 'Event Name'), ('section_name', 'Section Name'), ('row_name', 'Row name'), ('seat_num', 'Seat number'), ('last_seat', 'Last seat'), ('num_seats', 'Number seats'), ('acct_id', 'Account ID'), ('barcode', 'Barcode'), ('mobile', 'Mobile')], max_length=75, verbose_name='map column'),
        ),
    ]
