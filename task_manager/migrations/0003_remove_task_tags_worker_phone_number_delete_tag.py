# Generated by Django 4.2.3 on 2023-08-01 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0002_alter_worker_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='tags',
        ),
        migrations.AddField(
            model_name='worker',
            name='phone_number',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
