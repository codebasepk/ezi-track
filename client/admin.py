from django import forms
from django.contrib import admin
from django.utils.translation import gettext as _
from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from import_export.formats.base_formats import CSV, XLSX

from .models import Client


class ClientAdminForm(forms.ModelForm):
    inv_ref_1 = forms.CharField(required=True, max_length=50, label="INV REF 1")
    inv_ref_2 = forms.CharField(required=False, max_length=50, label="INV REF 2")
    inv_ref_3 = forms.CharField(required=False, max_length=50, label="INV REF 3")
    inv_ref_4 = forms.CharField(required=False, max_length=50, label="INV REF 4")
    inv_ref_5 = forms.CharField(required=False, max_length=50, label="INV REF 5")

    rcp_ref_1 = forms.CharField(required=True, max_length=50, label="RCP REF 1")
    rcp_ref_2 = forms.CharField(required=False, max_length=50, label="RCP REF 2")
    rcp_ref_3 = forms.CharField(required=False, max_length=50, label="RCP REF 3")
    rcp_ref_4 = forms.CharField(required=False, max_length=50, label="RCP REF 4")
    rcp_ref_5 = forms.CharField(required=False, max_length=50, label="RCP REF 5")

    class Meta:
        model = Client
        exclude = ('sage_invoice_reference', 'sage_payment_reference')  # Exclude the original fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Repopulate fields from semicolon-separated values if the instance already exists
        if self.instance.pk:
            # Split the sage_invoice_reference into individual fields
            inv_refs = self.instance.sage_invoice_reference.split(';')
            for i in range(len(inv_refs)):
                if i < 5:  # Only populate the first 5 inv_ref fields
                    self.fields[f'inv_ref_{i+1}'].initial = inv_refs[i]

            # Split the sage_payment_reference into individual fields
            rcp_refs = self.instance.sage_payment_reference.split(';')
            for i in range(len(rcp_refs)):
                if i < 5:  # Only populate the first 5 rcp_ref fields
                    self.fields[f'rcp_ref_{i+1}'].initial = rcp_refs[i]

    def clean(self):
        cleaned_data = super().clean()

        # Join all invoice references with a semicolon
        invoice_refs = [
            cleaned_data.get(f'inv_ref_{i}')
            for i in range(1, 6)
            if cleaned_data.get(f'inv_ref_{i}')
        ]
        cleaned_data['sage_invoice_reference'] = ';'.join(invoice_refs)

        # Join all payment references with a semicolon
        payment_refs = [
            cleaned_data.get(f'rcp_ref_{i}')
            for i in range(1, 6)
            if cleaned_data.get(f'rcp_ref_{i}')
        ]
        cleaned_data['sage_payment_reference'] = ';'.join(payment_refs)

        return cleaned_data


class ClientResource(ModelResource):
    class Meta:
        # Set the model to be used for the resource
        model = Client

        # Exclude following fields from export
        exclude = (
            'id', 'added', 'tracker_activation_date',
            'tracker_status_note', 'sim_active', 'sim_status_note',
            'sim_code', 'sage_invoice_reference', 'sage_payment_reference',
            'description', 'created_at'
        )

        # Set export field order
        export_order = (
            'email', 'sage_details', 'tracker_imei', 'expire_date', 'tracker_expire_date',
            'sim_number', 'sim_exp_date', 'sim_expire', 'sim_provider', 'tracker_status',
            'tracker_model', 'sold_by', 'country', 'status'
        )

    def get_export_headers(self, fields=None, selected_fields=None):
        """
        Returns a list of headers to be used in the export file.
        Uses the verbose name of each field in the export fields.
        """
        headers = []
        # If selected_fields is provided, use it; otherwise, use all export fields
        if selected_fields:
            fields = selected_fields
        else:
            fields = self.get_export_fields()

        for field in fields:
            # Get the verbose name of the field from the model's meta data
            headers.append(self.Meta.model._meta.get_field(field).verbose_name)
        return headers


class ClientAdmin(ExportMixin, admin.ModelAdmin):
    form = ClientAdminForm  # Use the custom form

    fieldsets = (
        (None, {
            'fields': (
                'added',
                'email',
                'sage_details',
                'tracker_imei',
                'tracker_activation_date',
                'expire_date',
                'tracker_expire_date',
                'tracker_status',
                'tracker_status_note',
                'sim_number',
                'sim_active',
                'sim_exp_date',
                'sim_expire',
                'status',
                'sim_status_note',
                'sim_provider',
                'sim_code',
                'tracker_model',
                'sold_by',
                'country',
                'description',
            )
        }),
        ('SAGE INVOICE REFERENCE', {
            'fields': (
                'inv_ref_1',
                'inv_ref_2',
                'inv_ref_3',
                'inv_ref_4',
                'inv_ref_5',
            )
        }),
        ('SAGE PAYMENT REFERENCE', {
            'fields': (
                'rcp_ref_1',
                'rcp_ref_2',
                'rcp_ref_3',
                'rcp_ref_4',
                'rcp_ref_5',
            )
        }),
    )

    def save_model(self, request, obj, form, change):
        # Save concatenated fields back to the original fields
        obj.sage_invoice_reference = form.cleaned_data['sage_invoice_reference']
        obj.sage_payment_reference = form.cleaned_data['sage_payment_reference']
        super().save_model(request, obj, form, change)

    # Set export formats
    formats = [CSV, XLSX]

    # Set export resource class
    resource_class = ClientResource

    # Set the fields to be displayed in the list view of the admin
    list_display = (
        'email', 'sage_details', 'tracker_imei', 'expire_date', 'tracker_expire_date',
        'sim_number', 'sim_exp_date', 'sim_expire', 'sim_provider', 'tracker_status',
        'tracker_model', 'sold_by', 'country', 'status'
    )

    # Add search fields for the admin
    search_fields = [
        'email', 'sage_details', 'tracker_imei', 'expire_date', 'sim_number',
        'sim_exp_date', 'tracker_model', 'sim_provider', 'tracker_status', 'status',
        'sold_by', 'sage_invoice_reference', 'sage_payment_reference'
    ]

    # Define list filter fields
    list_filter = (
        'status', 'tracker_status', 'expire_date', 'sim_exp_date', 'sold_by',
        'sim_provider', 'tracker_model', 'country'
    )


# Register the Client model with the custom admin class
admin.site.register(Client, ClientAdmin)
