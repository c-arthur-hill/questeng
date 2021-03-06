# Generated by Django 2.1.4 on 2019-02-09 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='upvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='articlepart',
            name='ordering',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='topic',
            name='total_downvotes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='topic',
            name='total_upvotes',
            field=models.IntegerField(default=0),
        ),
    ]
