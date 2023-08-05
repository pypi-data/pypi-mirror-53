from django.db import models


class DpSettings(models.Model):

    app_name = models.CharField(max_length=255, blank=False, null=False)
    key = models.CharField(max_length=255, blank=False, null=False)
    value_int = models.IntegerField(blank=True, null=True)
    value_string = models.TextField(blank=True, null=True)

    creation_date = models.DateTimeField(
        blank=True, null=True, auto_now_add=True)
    modification_date = models.DateTimeField(
        blank=True, null=True, auto_now=True)

    class Meta:
        
        db_table = 'dp_settings'
