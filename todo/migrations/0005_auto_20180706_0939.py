# Generated by Django 2.0.7 on 2018-07-06 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20180702_0635'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('content', 'list')},
        ),
    ]
