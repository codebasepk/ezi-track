from django import forms

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