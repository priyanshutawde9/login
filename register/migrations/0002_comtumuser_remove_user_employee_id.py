# Generated by Django 4.2.5 on 2023-11-02 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComtumUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('employee_id', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='employee_id',
        ),
    ]
