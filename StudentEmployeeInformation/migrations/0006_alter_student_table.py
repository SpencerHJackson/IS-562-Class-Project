# Generated by Django 4.1.2 on 2022-11-04 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('StudentEmployeeInformation', '0005_rename_students_student_alter_student_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='student',
            table='student_employee',
        ),
    ]
