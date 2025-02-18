# Generated by Django 5.1.4 on 2024-12-26 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estore_app', '0002_alter_product_cat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(max_length=100, verbose_name='Category Name')),
                ('cimage', models.ImageField(upload_to='image')),
            ],
        ),
    ]
