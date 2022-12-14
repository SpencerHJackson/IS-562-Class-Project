# Generated by Django 4.1.2 on 2022-11-04 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudentEmployeeInformation', '0012_alter_student_ta_assignments'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentEmployeePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'student_position',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='YearInProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_year', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'db_table': 'student_year',
                'ordering': ['student_year'],
            },
        ),
        migrations.RemoveField(
            model_name='student',
            name='calendar_year',
        ),
        migrations.RemoveField(
            model_name='student',
            name='class_code',
        ),
        migrations.RemoveField(
            model_name='student',
            name='semester',
        ),
        migrations.AlterField(
            model_name='student',
            name='employee_record',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_pay_increase',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='StudentEmployeeInformation.professor'),
        ),
        migrations.AlterModelTable(
            name='professor',
            table='is_faculty',
        ),
        migrations.AlterField(
            model_name='student',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='StudentEmployeeInformation.studentemployeeposition'),
        ),
        migrations.AlterField(
            model_name='student',
            name='year_in_program',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='StudentEmployeeInformation.yearinprogram'),
        ),
    ]
