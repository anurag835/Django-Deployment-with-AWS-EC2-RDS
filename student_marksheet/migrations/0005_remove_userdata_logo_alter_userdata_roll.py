# Generated by Django 4.2.5 on 2023-10-12 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_marksheet', '0004_userdata_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='logo',
        ),
        migrations.AlterField(
            model_name='userdata',
            name='roll',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
