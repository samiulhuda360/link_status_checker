from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', null=True)
    link_created = models.DateField(verbose_name='Link Creation Date')
    target_link = models.URLField(verbose_name='Target Link', null=True)
    link_to = models.URLField(verbose_name='Link To')
    anchor_text = models.CharField(max_length=255, verbose_name='Anchor Text')
    
    # Constants for choices
    dofollow = 'Dofollow'
    nofollow = 'Nofollow'
    source_removed = 'Source Removed'
    link_removed = 'Link Removed'
    Index_Check_Interval = 'Index_Check_Interval'
    
    STATUS_CHOICES = [
        (dofollow, 'Dofollow'),
        (nofollow, 'Nofollow'),
        (source_removed, 'Source Removed'),
        (link_removed, 'Link Removed'),
        (Index_Check_Interval, 'Index_Check_Interval'),
    ]

    status_of_link = models.CharField(
        max_length=25, 
        choices=STATUS_CHOICES,
        verbose_name='Status of Link', blank=True, null=True)
    
    index = "Index"
    not_index = "Not Index"
    INDEX_CHOICE = [
        (index, 'Indexed'),
        (not_index, 'Not Index'),
    ]
    index_status = models.CharField(
        max_length=11, 
        choices=INDEX_CHOICE,
        verbose_name='Index Status', blank=True, null=True)
    
    last_index_check = models.DateField(verbose_name='Last Index Check', null=True, blank=True)

    last_crawl_date = models.DateField(verbose_name='Last Crawl Date', null=True, blank=True)
    manual_edit = models.BooleanField(default=False)
    # Constants for address_status choices
    ADDRESS_STATUS_CHOICES = [
        ('-', '-'),
        ('addressed', 'Addressed'),
    ]

    # Adding the address_status field
    address_status = models.CharField(
        max_length=10, 
        choices=ADDRESS_STATUS_CHOICES,
        default='-', 
        verbose_name='Address Status',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'target_link', 'link_to', 'anchor_text'], name='unique_link_combination')
        ]

class LinkStatusThreshold(models.Model):
    status = models.CharField(max_length=25, choices=Link.STATUS_CHOICES, verbose_name='Link Status')
    days_threshold = models.IntegerField(default=2, verbose_name='Days Threshold')

    def __str__(self):
        return f"{self.status}: {self.days_threshold} days"

class Index_checker_api(models.Model):
    key = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if Index_checker_api.objects.exists() and not self.pk:
            raise models.ValidationError('There is already an API Key set.')
        super().save(*args, **kwargs)

    def __str__(self):
        return "API Key"

    class Meta:
        verbose_name_plural = "API Key"