# Generated by Django 4.2.3 on 2023-07-22 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_delete_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='EnRuDictionary',
        ),
        migrations.DeleteModel(
            name='Phrase',
        ),
    ]
