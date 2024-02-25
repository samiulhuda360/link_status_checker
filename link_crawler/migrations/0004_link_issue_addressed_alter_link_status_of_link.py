# Generated by Django 5.0.2 on 2024-02-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_crawler', '0003_alter_link_status_of_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='issue_addressed',
            field=models.BooleanField(blank=True, null=True, verbose_name='Issue Addressed'),
        ),
        migrations.AlterField(
            model_name='link',
            name='status_of_link',
            field=models.CharField(blank=True, choices=[('Live - Dofollow', 'Live - Dofollow'), ('Live - Nofollow', 'Live - Nofollow'), ('Source Removed', 'Source Removed'), ('Link Removed', 'Link Removed')], max_length=15, null=True, verbose_name='Status of Link'),
        ),
    ]