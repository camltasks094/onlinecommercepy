# Generated by Django 5.1 on 2024-08-24 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlinecommerceApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tienda',
            name='id_direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='detalledomicilio',
            name='id_direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AlterField(
            model_name='tienda',
            name='imagen',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name='Direccion',
        ),
    ]
