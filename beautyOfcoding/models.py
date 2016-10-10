# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Lottery(models.Model):
    present_level = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    micro_id = models.BigIntegerField(unique=True, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    hash_id = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'lottery'
