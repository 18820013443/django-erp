# Generated by Django 3.1.3 on 2021-04-17 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersdetail',
            name='order_header',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='sales.ordersheader'),
        ),
    ]
