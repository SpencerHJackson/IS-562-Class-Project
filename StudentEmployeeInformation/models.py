# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Students(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    international = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    semester = models.CharField(max_length=255, blank=True, null=True)
    calendaryear = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    byuid = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    class_code = models.CharField(max_length=255, blank=True, null=True)
    employee_record = models.CharField(max_length=255, blank=True, null=True)
    supervisor = models.CharField(max_length=255, blank=True, null=True)
    hiredate = models.CharField(max_length=255, blank=True, null=True)
    payrate = models.CharField(max_length=100, blank=True, null=True)
    lastpayincrease = models.CharField(max_length=255, blank=True, null=True)
    payincreaseamount = models.CharField(max_length=100, blank=True, null=True)
    increaseinputdate = models.CharField(max_length=255, blank=True, null=True)
    yearinprogram = models.CharField(max_length=255, blank=True, null=True)
    paygradtuition = models.CharField(max_length=255, blank=True, null=True)
    isterminated = models.CharField(max_length=255, blank=True, null=True)
    terminateddate = models.CharField(max_length=255, blank=True, null=True)
    qualtricssent = models.CharField(max_length=255, blank=True, null=True)
    eform = models.CharField(max_length=255, blank=True, null=True)
    eformdate = models.CharField(max_length=255, blank=True, null=True)
    workauth = models.CharField(max_length=255, blank=True, null=True)
    workauthdate = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'students'
