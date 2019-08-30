from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ParserConfigurationDef, ParserCollection
from extra_views import CreateWithInlinesView, \
    UpdateWithInlinesView, InlineFormSetFactory, \
    NamedFormsetsMixin

from .forms import ColumnMapInineView, \
    ParserConfigurationDefForm, get_columnmap_inline_view

class ParserListView(LoginRequiredMixin, ListView):
    model = ParserConfigurationDef
    template_name = 'parser_conf/parsers_list.html'


    def get_queryset(self):
        u = self.request.user
        if not u.is_staff:
            return self.model.objects.filter(user=u) ## todo: combined another which shared option as an public
        return super(ParserListView, self).get_queryset()


    def get_context_data(self, **kwargs):
        context = super(ParserListView, self).get_context_data(**kwargs)
        context['page_header'] = 'Parsers'
        return context


class ParserUpdateWithInlineView(LoginRequiredMixin, NamedFormsetsMixin, UpdateWithInlinesView):
    model = ParserConfigurationDef
    fields = ['name', ]
    inlines_names = ['column_map_formset', ]
    template_name = 'parser_conf/parser_form.html'


    def get_context_data(self, **kwargs):
        context = super(ParserUpdateWithInlineView, self).get_context_data(**kwargs)
        context['page_header'] = 'Parsers'
        return context

    def get_form_class(self):
        return ParserConfigurationDefForm

    def get_success_url(self):
        return reverse('parser:parser_edit', args=[self.object.pk, ])

    def get_inlines(self):
        column_map_inlines = get_columnmap_inline_view(self.object.collection.pk)
        return [column_map_inlines, ]

class ParserCreateWithInlineView(LoginRequiredMixin, NamedFormsetsMixin, CreateWithInlinesView):
    model = ParserConfigurationDef
    collection_id = None
    fields = ['name', ]
    # inlines = [ColumnMapInineView, ]
    inlines_names = ['column_map_formset', ]
    template_name = 'parser_conf/parser_form.html'

    def dispatch(self, request, *args, **kwargs):
        collection_id = kwargs['collection_id']
        self.collection_id = ParserCollection.objects.get(pk=collection_id)
        return super(ParserCreateWithInlineView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParserCreateWithInlineView, self).get_context_data(**kwargs)
        context['page_header'] = 'Parsers'
        return context

    def get_success_url(self):
        return reverse('parser:parser_edit', args=[self.object.pk, ])

    def get_form_class(self):
        return ParserConfigurationDefForm

    def get_inlines(self):
        column_map_inlines = get_columnmap_inline_view(self.collection_id.pk)
        return [column_map_inlines, ]

    def forms_valid(self, form, inlines):
        print("called form valid")
        obj = form.save(commit=False)
        obj.collection = self.collection_id
        obj.user = self.request.user
        obj.save()
        return super(ParserCreateWithInlineView, self).forms_valid(form, inlines)

class CollectionListView(ListView):
    model = ParserCollection
    template_name = 'parser_conf/collection_list.html'

    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        context['page_header'] = 'Collections'
        return context

