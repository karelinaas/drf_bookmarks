# Generated by Django 3.2 on 2022-12-23 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('time_deleted', models.DateTimeField(null=True)),
                ('favicon', models.URLField(null=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='bookmark',
            constraint=models.UniqueConstraint(condition=models.Q(time_deleted__isnull=True), fields=('url',), name='URL_UNIQUE_IF_NOT_DELETED'),
        ),
    ]
