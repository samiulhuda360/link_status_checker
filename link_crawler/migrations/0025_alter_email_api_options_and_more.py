# Generated by Django 4.2.7 on 2024-04-25 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_crawler', '0024_domain_blogger_details_remove_link_blogger_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='email_api',
            options={'verbose_name_plural': 'Email Sender Details'},
        ),
        migrations.AlterModelOptions(
            name='index_checker_api',
            options={'verbose_name_plural': 'Index Checker API'},
        ),
        migrations.AddField(
            model_name='email_api',
            name='sender_email',
            field=models.EmailField(default='directors@searchcombat.com', max_length=254),
        ),
        migrations.AddField(
            model_name='email_api',
            name='sender_name',
            field=models.CharField(default='Search Combat Team', max_length=255),
        ),
    ]
