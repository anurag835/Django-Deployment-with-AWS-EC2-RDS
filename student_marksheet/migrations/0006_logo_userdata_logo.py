# Generated by Django 4.2.5 on 2023-10-12 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_marksheet', '0005_remove_userdata_logo_alter_userdata_roll'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='logos/')),
            ],
        ),
        migrations.AddField(
            model_name='userdata',
            name='logo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_marksheet.logo'),
        ),
    ]
