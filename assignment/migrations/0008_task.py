# Generated by Django 4.2.3 on 2023-07-20 07:21

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0007_alter_group_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', ckeditor.fields.RichTextField()),
                ('post_date', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(auto_now=True)),
            ],
        ),
    ]
