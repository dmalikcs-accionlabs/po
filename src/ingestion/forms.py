from utils.forms import BaseOnlyFormClassAdd

from django import forms
from parser_conf.models import ParserConfigurationDef
import magic
import tempfile
import os


def get_ingestion_form(user):
    p = ParserConfigurationDef.objects.filter(user=user)

    class _InventoryUploadForm(BaseOnlyFormClassAdd):
        parser = forms.ModelChoiceField(queryset=p, help_text="Please leave blank! if you are not sure", required=False)
        production_id = forms.IntegerField(widget=forms.NumberInput(attrs={'data-toggle': 'modal', 'data-target': '.bs-example-modal-lg'}), required=True)
        file = forms.FileField(help_text="Supported files: xls")
        mobile = forms.IntegerField(min_value=1000000000, max_value=9999999999, help_text='Send status report after processing - In progress')

        def clean(self):
            cleaned_data = super(_InventoryUploadForm, self).clean()
            attachment = cleaned_data.get('file')
            try:

                fd, tmp = tempfile.mkstemp()
                with os.fdopen(fd, 'wb+') as out:
                    for chunk in attachment.chunks():
                        out.write(chunk)
                with open(tmp, 'rb+') as inventory_file:
                    if not magic.from_buffer(inventory_file.read(), mime=True) \
                           in ['application/vnd.ms-office', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', ]:
                        print("Raise exception")
                        raise forms.ValidationError(
                            "Unsupported file format. Kindly upload inventory into xls format"
                        )
            finally:
                os.unlink(tmp)

            return cleaned_data

    return _InventoryUploadForm


class EventNameSearchForm(forms.Form):
    venue_name = forms.CharField(required=True)
    event_date = forms.DateField(required=True)
    event_time = forms.TimeField(required=True, input_formats=('%I:%M', ))
