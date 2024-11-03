from django.contrib import admin
from django.utils.translation import gettext as _
from import_export.resources import ModelResource
from import_export.admin import ExportMixin
from import_export.formats.base_formats import CSV, XLSX

from .models import Client


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
