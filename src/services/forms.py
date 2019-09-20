from django import forms
from utils.forms import BaseOnlyFormClassAdd



class EventNameSearchForm(BaseOnlyFormClassAdd):
    venue_name = forms.CharField(required=True)
    event_date = forms.DateField(required=True)
    event_time = forms.TimeField(required=True, input_formats=('%I:%M %p', ))
