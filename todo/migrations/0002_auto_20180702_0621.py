# Generated by Django 2.0.6 on 2018-07-02 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, help_text="When it's created", verbose_name='Create time')),
            ],
            options={
                'verbose_name': 'To-Do List',
                'verbose_name_plural': 'To-Do Lists',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='list',
            field=models.ForeignKey(blank=True, help_text='The list where the item belongs to', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='todo.List', verbose_name='List'),
        ),
    ]
