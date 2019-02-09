# Generated by Django 2.1.4 on 2019-02-08 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=255)),
                ('upvotes', models.IntegerField()),
                ('downvotes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ArticlePart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_type', models.CharField(choices=[('p', 'Paragraph'), ('h2', 'Large Header'), ('h3', 'Small Header')], max_length=255)),
                ('subheader', models.CharField(blank=True, max_length=255)),
                ('paragraph', models.TextField(blank=True)),
                ('ordering', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('approved', models.BooleanField(default=False)),
                ('total_upvotes', models.IntegerField()),
                ('total_downvotes', models.IntegerField()),
            ],
        ),
    ]
