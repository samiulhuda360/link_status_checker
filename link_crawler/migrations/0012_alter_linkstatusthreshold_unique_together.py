# Generated by Django 4.2.7 on 2024-03-02 21:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('link_crawler', '0011_alter_linkstatusthreshold_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='linkstatusthreshold',
            unique_together=set(),
        ),
    ]
