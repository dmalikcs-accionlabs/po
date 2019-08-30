_author__ = 'dmalik'

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


class BaseOnlyFormClassAdd(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BaseOnlyFormClassAdd, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if self.fields[field].widget.__class__.__name__ == 'DateInput':
                self.fields[field].widget.attrs['class'] = 'form-control hasDatepicker'
            elif self.fields[field].widget.__class__.__name__ == 'TimeInput':
                self.fields[field].widget.attrs['class'] = 'form-control clockpicker'

            elif self.fields[field].widget.__class__.__name__ == 'RangeWidget':
                self.fields[field].widget.attrs['class'] = 'form-control hasDatepicker'