# Generated by Django 5.0.4 on 2024-07-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrole',
            name='job_url',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobrole',
            name='job_id',
            field=models.CharField(max_length=50),
        ),
    ]
