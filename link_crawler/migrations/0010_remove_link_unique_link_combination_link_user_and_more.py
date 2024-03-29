# Generated by Django 4.2.7 on 2024-03-02 20:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('link_crawler', '0009_linkstatusthreshold'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='link',
            name='unique_link_combination',
        ),
        migrations.AddField(
            model_name='link',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AddField(
            model_name='linkstatusthreshold',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='linkstatusthreshold',
            name='status',
            field=models.CharField(choices=[('Dofollow', 'Dofollow'), ('Nofollow', 'Nofollow'), ('Source Removed', 'Source Removed'), ('Link Removed', 'Link Removed')], max_length=15, verbose_name='Link Status'),
        ),
        migrations.AlterUniqueTogether(
            name='linkstatusthreshold',
            unique_together={('user', 'status')},
        ),
        migrations.AddConstraint(
            model_name='link',
            constraint=models.UniqueConstraint(fields=('user', 'target_link', 'link_to', 'anchor_text'), name='unique_link_combination'),
        ),
    ]
