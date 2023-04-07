from django.db import models
from django.utils.translation import gettext as _


# Create your models here.
class Client(models.Model):
    email = models.EmailField(_('EMAIL'), max_length=100, unique=True)
    sage_details = models.CharField(_('SAGE DETAILS'), max_length=255)
    sim_number = models.CharField(_('SIM NUMBER'), max_length=255, unique=True)
    tracker_imei = models.CharField(_('TRACKER IMEI'), max_length=255, unique=True)
    added = models.DateField(_('ADDED'))
    sim_expire = models.CharField(_('SIM EXPIRE'), max_length=25)
    sim_provider = models.CharField(_('SIM PROVIDER'), max_length=25)
    description = models.TextField(_('EZITRACK DESCRIPTION'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
