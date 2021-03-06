# Generated by Django 2.0.6 on 2018-07-02 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0003_initial_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(help_text='The list where the item belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='todo.List', verbose_name='List'),
        ),
    ]
