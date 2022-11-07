# Generated by Django 4.1.2 on 2022-11-07 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentEmployeeInformation', '0024_auto_20221107_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='position',
        ),
        migrations.RemoveField(
            model_name='student',
            name='ra_history',
        ),
        migrations.RemoveField(
            model_name='student',
            name='supervisor',
        ),
        migrations.RemoveField(
            model_name='student',
            name='ta_history',
        ),
        migrations.AddField(
            model_name='student',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
