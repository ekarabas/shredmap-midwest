# Generated by Django 3.2.7 on 2022-02-16 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shredmap_midwest', '0005_auto_20220207_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='resort',
            name='avg_groomer',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='resort',
            name='avg_lift',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='resort',
            name='avg_park',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='resort',
            name='avg_vibe',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
    ]
