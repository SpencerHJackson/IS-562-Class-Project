# Generated by Django 4.1.2 on 2022-11-04 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudentEmployeeInformation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'is_professor',
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_name', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'season',
                'ordering': ['season_name'],
            },
        ),
        migrations.CreateModel(
            name='UniveristyClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('class_name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'is_class',
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='StudentEmployeeInformation.season')),
            ],
            options={
                'db_table': 'semester',
                'ordering': ['year'],
            },
        ),
        migrations.CreateModel(
            name='ClassSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='StudentEmployeeInformation.univeristyclass')),
                ('semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='StudentEmployeeInformation.semester')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='StudentEmployeeInformation.professor')),
            ],
            options={
                'db_table': 'class_section',
                'ordering': ['semester', 'course'],
            },
        ),
    ]
