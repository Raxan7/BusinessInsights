# Generated by Django 5.0.3 on 2024-04-22 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_delete_sales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('sales', 'sales'), ('on loan', 'on loan'), ('on order', 'on order')], max_length=50)),
            ],
        ),
    ]
