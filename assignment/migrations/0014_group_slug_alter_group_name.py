# Generated by Django 4.2.3 on 2023-07-20 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0013_alter_task_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
