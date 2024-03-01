from django.db import models

class Link(models.Model):
    link_created = models.DateField(verbose_name='Link Creation Date')
    target_link = models.URLField(verbose_name='Target Link', null=True)
    link_to = models.URLField(verbose_name='Link To')
    anchor_text = models.CharField(max_length=255, verbose_name='Anchor Text')
    
    dofollow = 'Dofollow'
    nofollow = 'Nofollow'
    source_removed = 'Source Removed'
    link_removed = 'Link Removed'
    


    STATUS_CHOICES = [
        (dofollow, 'Dofollow'),
        (nofollow, 'Nofollow'),
        (source_removed, 'Source Removed'),
        (link_removed, 'Link Removed'),
    ]

    status_of_link = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES,
        verbose_name='Status of Link', blank=True, null=True)
    
    index ="Index"
    not_index = "Not Index"
    INDEX_CHOICE = [
        (index, 'Indexed'),
        (not_index, 'Not Index'),
    ]
    index_status = models.CharField(
        max_length=11, 
        choices=INDEX_CHOICE,
        verbose_name='Index Status', blank=True, null=True)

    issue_addressed = models.BooleanField(verbose_name='Issue Addressed', blank=True, null=True)
    last_crawl_date = models.DateField(verbose_name='Last Crawl Date', null=True, blank=True)
    manual_edit = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['target_link', 'link_to', 'anchor_text'], name='unique_link_combination')
        ]


  
