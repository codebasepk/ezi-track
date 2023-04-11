from django.db import models
from django.utils.translation import gettext as _

SIM_PROVIDER = (
    ("VODACOM", "VODACOM"),
    ("FLOLIVE", "FLOLIVE"),
    ("MTN", "MTN"),
)


# Create your models here.
class Client(models.Model):
    expire_date = models.CharField(_('EXPIRE DATE'), max_length=255)
    email = models.EmailField(_('EMAIL'), max_length=100)
    sage_details = models.CharField(_('SAGE DETAILS'), max_length=255)
    sim_number = models.CharField(_('SIM NUMBER'), max_length=255, unique=True)
    tracker_imei = models.CharField(_('TRACKER IMEI'), max_length=255, unique=True)
    added = models.DateField(_('ADDED'))
    sim_expire = models.DateField(_('SIM EXPIRE'))
    sim_provider = models.CharField(_('SIM PROVIDER'), max_length=25, choices=SIM_PROVIDER)
    description = models.TextField(_('EZITRACK DESCRIPTION'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email