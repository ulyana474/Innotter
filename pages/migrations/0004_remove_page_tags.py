# Generated by Django 4.1.3 on 2022-11-14 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_alter_page_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='tags',
        ),
    ]
