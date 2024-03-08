# Generated by Django 4.2.7 on 2024-03-08 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_crawler', '0017_link_address_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link',
            name='issue_addressed',
        ),
        migrations.AlterField(
            model_name='link',
            name='address_status',
            field=models.CharField(choices=[('-', '-'), ('addressed', 'Addressed')], default='-', max_length=10, verbose_name='Address Status'),
        ),
    ]