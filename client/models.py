from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django_countries.fields import CountryField

EXPIRE_DATE = [
    (f"EXP{month}{year}", f"EXP{month}{year}")
    for year in range(24, 36)
    for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
]

SIM_PROVIDER = (
    ("FLOLIVE_RSA", "FLOLIVE – RSA NEIGHBOURS"),
    ("FLOLIVE_SSA", "FLOLIVE – SUB-SAHARAN AFRICA"),
    ("FLICKSWITCH_VODACOM", "FLICKSWITCH - VODACOM"),
    ("FLICKSWITCH_MTN", "FLICKSWITCH – MTN"),
    ("FLICKSWITCH_OTHER", "FLICKSWITCH - OTHER"),
    ("CLIENT_OWN", "CLIENT - OWN SIM"),
    ("OTHER", "OTHER"),
)

SIM_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("SUSPENDED", "SUSPENDED"),
)

SOLD_BY = (
    ("TAKEALOT", "TAKEALOT"),
    ("EZITRACK_DIRECT_SALE", "EZITRACK DIRECT SALE"),
    ("AMAZON", "AMAZON"),
    ("OTHER", "OTHER"),
    ("EZITRACK_DEALER", "EZITRACK DEALER"),
)

SIM_CODE = (
    ("ESC", "ESC – FLOLIVE EZITRACK SIMCONTROL"),
    ("EFSC", "EFSC – FLICKSWITCH SIM CONTROL"),
    ("PRIV", "PRIV – PRIVATE SIM"),
    ("OTHER", "Other"),
)


class Client(models.Model):
    expire_date = models.CharField(_('EXPIRE DATE'), max_length=8, choices=EXPIRE_DATE)
    email = models.EmailField(_('EMAIL'), max_length=100)
    sage_details = models.CharField(_('SAGE DETAILS'), max_length=255)
    sim_number = models.CharField(_('SIM NUMBER'), max_length=255, unique=True)
    tracker_imei = models.CharField(_('TRACKER IMEI'), max_length=255, unique=True)
    added = models.DateField(_('ADDED'), null=True)
    sim_expire = models.DateField(_('SIM EXPIRE'), null=True)
    sim_provider = models.CharField(_('SIM NETWORK'), max_length=50, choices=SIM_PROVIDER)
    status = models.CharField(_('SIM STATUS'), max_length=25, choices=SIM_STATUS, default="ACTIVE")
    activated_at = models.DateTimeField(_('ACTIVATED AT'), null=True, blank=True)
    suspended_at = models.DateTimeField(_('SUSPENDED AT'), null=True, blank=True)
    sage_invoice_reference = models.CharField(_('SAGE INVOICE REFERENCE'), max_length=50, blank=True)
    sage_payment_reference = models.CharField(_('SAGE PAYMENT REFERENCE'), max_length=50, blank=True)
    tracker_model = models.CharField(_('TRACKER MODEL'), max_length=255)
    country = CountryField(_('COUNTRY'))
    sold_by = models.CharField(_('SOLD BY'), max_length=25, choices=SOLD_BY)
    sim_code = models.CharField(_('SIM CODE'), max_length=5, choices=SIM_CODE)
    description = models.TextField(_('EZITRACK DESCRIPTION'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_instance = Client.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                if self.status == "ACTIVE":
                    self.activated_at = timezone.now()
                    self.suspended_at = None
                elif self.status == "SUSPENDED":
                    self.suspended_at = timezone.now()
        else:
            if self.status == "ACTIVE":
                self.activated_at = timezone.now()
            elif self.status == "SUSPENDED":
                self.suspended_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email