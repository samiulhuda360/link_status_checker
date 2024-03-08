# Generated by Django 4.2.7 on 2024-03-08 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_crawler', '0015_alter_index_checker_api_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='status_of_link',
            field=models.CharField(blank=True, choices=[('Dofollow', 'Dofollow'), ('Nofollow', 'Nofollow'), ('Source Removed', 'Source Removed'), ('Link Removed', 'Link Removed'), ('Index_Check_Interval', 'Index_Check_Interval')], max_length=25, null=True, verbose_name='Status of Link'),
        ),
        migrations.AlterField(
            model_name='linkstatusthreshold',
            name='status',
            field=models.CharField(choices=[('Dofollow', 'Dofollow'), ('Nofollow', 'Nofollow'), ('Source Removed', 'Source Removed'), ('Link Removed', 'Link Removed'), ('Index_Check_Interval', 'Index_Check_Interval')], max_length=25, verbose_name='Link Status'),
        ),
    ]