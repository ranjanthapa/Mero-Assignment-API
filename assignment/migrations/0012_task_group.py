# Generated by Django 4.2.3 on 2023-07-20 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0011_alter_task_due_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='assignment.group'),
        ),
    ]