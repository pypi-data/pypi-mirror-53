# Generated by Django 2.1.8 on 2019-08-13 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saleboxdjango', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='boolean_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='boolean_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='boolean_3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='boolean_4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='boolean_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='boolean_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='boolean_3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='boolean_4',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='boolean_1',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='boolean_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='boolean_3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productvariant',
            name='boolean_4',
            field=models.BooleanField(default=False),
        ),
    ]
