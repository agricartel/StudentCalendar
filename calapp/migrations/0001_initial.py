# Generated by Django 2.2.2 on 2019-09-28 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=300)),
                ('color_hex', models.CharField(max_length=6)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.Category')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('pass_hash', models.CharField(max_length=128)),
                ('pass_salt', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=300)),
                ('deadline', models.DateTimeField()),
                ('priority', models.CharField(choices=[('HIGH_PRI', 'High'), ('MED_PRI', 'Medium'), ('LOW_PRI', 'Low')], default='MED_PRI', max_length=15)),
                ('completed', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.User')),
            ],
        ),
        migrations.CreateModel(
            name='Subtasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtask_name', models.CharField(max_length=300)),
                ('completed', models.BooleanField()),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.Tasks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.User')),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=300)),
                ('start_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.Category')),
                ('parent_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.Tasks')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.User')),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calapp.User'),
        ),
    ]