# Generated by Django 4.2.3 on 2023-08-02 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_category_description_definition_categories'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
    ]
