from extra_views import CreateWithInlinesView, \
    UpdateWithInlinesView, InlineFormSetFactory, \
    NamedFormsetsMixin
from .models import ParserConfigurationDef, ColumnPayloadMap, \
    ParserCollection
from utils.forms import BaseFormClassAdd
from django import forms


class ParserConfigurationDefForm(BaseFormClassAdd):


    class Meta:
        model = ParserConfigurationDef
        fields = ['name', ]


class ColumnMapForm(BaseFormClassAdd):


    class Meta:
        model = ColumnPayloadMap
        fields = ['column_name', 'payload', ]


class ColumnMapInineView(InlineFormSetFactory):
        model = ColumnPayloadMap
        fields = ['column_name', 'payload', ]
        form_class = ColumnMapForm



def  get_column_map_form(collection_id):
    parser = ParserCollection.objects.get(id=collection_id)
    choices = [('','---------'),] + \
              [(column, display_column)for column, display_column in parser.columns.items()]

    class _ColumnMapForm(BaseFormClassAdd):
        payload = forms.ChoiceField(choices=choices)

        class Meta:
            model = ColumnPayloadMap
            fields = ['column_name', 'payload', ]
    return _ColumnMapForm



def get_columnmap_inline_view(collection_id):
    column_map_form = get_column_map_form(collection_id)

    class _ColumnMapInineView(InlineFormSetFactory):
        model = ColumnPayloadMap
        fields = ['column_name', 'payload', ]
        form_class = column_map_form
        factory_kwargs = {
            'extra': 10,
        }

    return _ColumnMapInineView
