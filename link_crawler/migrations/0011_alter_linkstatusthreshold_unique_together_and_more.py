# Generated by Django 4.2.7 on 2024-03-02 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('link_crawler', '0010_remove_link_unique_link_combination_link_user_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='linkstatusthreshold',
            unique_together={('status',)},
        ),
        migrations.RemoveField(
            model_name='linkstatusthreshold',
            name='user',
        ),
    ]