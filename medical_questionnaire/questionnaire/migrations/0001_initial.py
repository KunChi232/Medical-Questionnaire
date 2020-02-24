# Generated by Django 3.0.3 on 2020-02-24 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_type', models.TextField()),
                ('name', models.TextField()),
                ('wellcome', models.TextField()),
                ('questions', models.TextField()),
                ('summary', models.TextField()),
            ],
            options={
                'db_table': 'question',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.TextField()),
                ('session_id', models.TextField()),
                ('question_type', models.TextField()),
                ('name', models.TextField()),
                ('user_select', models.TextField()),
                ('next_question', models.IntegerField()),
                ('complete', models.IntegerField()),
                ('create_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.TextField()),
                ('scores', models.TextField()),
                ('current_session', models.TextField()),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
    ]
