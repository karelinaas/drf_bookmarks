# Generated by Django 3.2 on 2023-07-17 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookmarks', '0002_auto_20230710_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookmarks', to='bookmarks.group'),
        ),
    ]
