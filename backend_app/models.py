from django.db import models
from django.utils import timezone


class UserDetails(models.Model):
    GENDER_CHOICE = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    WHATSAPP_CHOICE = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    mobile_number = models.CharField(max_length=20, null=False, blank=False)
    email = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICE, default='Male', max_length=6)
    registered_at = models.DateTimeField(default=timezone.now)
    is_active = models.IntegerField(default=1, null=False, blank=False)
    is_whatsApp = models.CharField(choices=WHATSAPP_CHOICE, default='Yes', max_length=3)
    last_login_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    created_by = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = "user_details"


class UserToken(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=2500, null=False, blank=False)
    user_id = models.IntegerField(null=False, blank=True)

    class Meta:
        db_table = "user_token"


class UserMapping(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.IntegerField(null=False, blank=False)
    user_id = models.IntegerField(null=False, blank=False)

    class Meta:
        db_table = "user_mapping"


class UserTypes(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = "user_types"


class MarkSheet(models.Model):
    CHOICE = [
        ('New', 'New'),
        ('Inprogress', 'Inprogress'),
        ('Done', 'Done'),
        ('Failed', 'Failed')
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, null=False, blank=False)
    gender = models.CharField(max_length=5)
    age = models.IntegerField(null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    marks = models.JSONField(null=True, blank=True)
    creation_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=CHOICE, default="New")

    class Meta:
        db_table = "mark_sheet"

