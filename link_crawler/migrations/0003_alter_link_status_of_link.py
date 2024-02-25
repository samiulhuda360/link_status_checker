# Generated by Django 5.0.2 on 2024-02-20 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_crawler', '0002_remove_link_link_taken_from_link_target_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='status_of_link',
            field=models.CharField(choices=[('Live - Dofollow', 'Live - Dofollow'), ('Live - Nofollow', 'Live - Nofollow'), ('Source Removed', 'Source Removed'), ('Link Removed', 'Link Removed')], default='Live - Dofollow', max_length=15, verbose_name='Status of Link'),
        ),
    ]