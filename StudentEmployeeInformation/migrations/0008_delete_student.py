# Generated by Django 4.1.2 on 2022-11-04 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StudentEmployeeInformation', '0007_rename_byuid_student_byu_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
    ]
