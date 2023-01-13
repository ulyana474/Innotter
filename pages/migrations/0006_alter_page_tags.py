# Generated by Django 4.1.3 on 2022-11-16 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_tag'),
        ('pages', '0005_page_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='pages_tags', to='users.tag'),
        ),
    ]
