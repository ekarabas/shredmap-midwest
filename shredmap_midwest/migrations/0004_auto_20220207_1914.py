# Generated by Django 3.2.7 on 2022-02-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shredmap_midwest', '0003_auto_20220207_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='groomer_review',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='review',
            name='lift_review',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='review',
            name='message',
            field=models.TextField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='review',
            name='park_review',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='review',
            name='vibe_review',
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
