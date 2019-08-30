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
        file = forms.FileField(help_text="Supported files: xls")

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
                            in ['application/vnd.ms-office', ]:
                        print("Raise exception")
                        raise forms.ValidationError(
                            "Unsupported file format. Kindly upload inventory into xls format"
                        )
            finally:
                os.unlink(tmp)

            return cleaned_data

    return _InventoryUploadForm