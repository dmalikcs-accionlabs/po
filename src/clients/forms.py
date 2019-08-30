from .models import Client, ClientAgent
from django import forms


class BaseFormClassAdd(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseFormClassAdd, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if self.fields[field].widget.__class__.__name__ == 'DateInput':
                self.fields[field].widget.attrs['class'] = 'form-control hasDatepicker'
            elif self.fields[field].widget.__class__.__name__ == 'TimeInput':
                self.fields[field].widget.attrs['class'] = 'form-control clockpicker'

class ClientForm(BaseFormClassAdd):

    class Meta:
        model = Client
        fields = ['name', 'external_clientid', 'parser', ]


class ClientAgentForm(BaseFormClassAdd):

    class Meta:
        model = ClientAgent
        fields = ['client', 'name', 'email', 'is_logged_allowed', ]