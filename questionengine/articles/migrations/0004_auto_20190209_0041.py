# Generated by Django 2.1.4 on 2019-02-09 00:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('articles', '0003_auto_20190209_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='articles.Topic'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
