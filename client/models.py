from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django_countries.fields import CountryField

SIM_EXPIRE_DATE = [
    (f"SEXP{month}{year}", f"SEXP{month}{year}")
    for year in range(24, 36)
    for month in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
]

TRACKER_EXPIRE_DATE = [
    (f"TEXP{month}{year}", f"TEXP{month}{year}")
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

STATUS = (
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
    added = models.DateField(_('ADDED'))
    email = models.EmailField(_('EZIMAP USER ACCOUNT'), max_length=100)
    sage_details = models.CharField(_('SAGE ACCOUNT'), max_length=255)
    tracker_imei = models.CharField(_('TRACKER IMEI'), max_length=255, unique=True)
    tracker_activation_date = models.DateField(_('TRACKER ACTIVATION DATE'))
    expire_date = models.CharField(_('TRACKER EXP DATE'), max_length=9, choices=TRACKER_EXPIRE_DATE)
    tracker_expire_date = models.DateField(_('TRACKER EXPIRE DATE'))
    tracker_status = models.CharField(_('TRACKER STATUS'), max_length=25, choices=STATUS, default="ACTIVE")
    tracker_status_note = models.TextField(_('TRACKER STATUS NOTE'), null=True, blank=True)
    sim_number = models.CharField(_('SIM NUMBER'), max_length=255, unique=True)
    sim_active = models.DateField(_('SIM ACTIVATION DATE'))
    sim_exp_date = models.CharField(_('SIM EXP DATE'), max_length=9, choices=SIM_EXPIRE_DATE)
    sim_expire = models.DateField(_('SIM EXPIRE DATE'))
    status = models.CharField(_('SIM STATUS'), max_length=25, choices=STATUS, default="ACTIVE")
    sim_status_note = models.TextField(_('SIM STATUS NOTE'), null=True, blank=True)
    sim_provider = models.CharField(_('SIM NETWORK'), max_length=50, choices=SIM_PROVIDER)
    sim_code = models.CharField(_('SIM CODE'), max_length=5, choices=SIM_CODE)
    tracker_model = models.CharField(_('TRACKER MODEL'), max_length=255)
    sold_by = models.CharField(_('SOLD BY'), max_length=25, choices=SOLD_BY)
    country = CountryField(_('COUNTRY IN USE'))
    sage_invoice_reference = models.CharField(_('SAGE INVOICE REFERENCE'), max_length=50, blank=True)
    sage_payment_reference = models.CharField(_('SAGE PAYMENT REFERENCE'), max_length=50, blank=True)
    description = models.TextField(_('ADDITIONAL NOTES'), null=True, blank=True)
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