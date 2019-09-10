from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, \
    DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import SingleObjectMixin
from .models import ParserConfigurationDef, ParserCollection, \
    EmailNotification, PostIngestionReport
from extra_views import CreateWithInlinesView, \
    UpdateWithInlinesView, InlineFormSetFactory, \
    NamedFormsetsMixin
from extra_views import ModelFormSetView
from .forms import ColumnMapInineView, \
    ParserConfigurationDefForm, get_columnmap_inline_view, \
    EmailNotificationForm, PostIngestionReportForm
from django.utils.html import format_html


class ParserListView(LoginRequiredMixin, ListView):
    template_name = 'parser_conf/parsers_list.html'
    queryset = ParserConfigurationDef. \
        objects.filter(deleted_at__isnull=True)

    def get_queryset(self):
        u = self.request.user
        if not u.is_staff:
            return self.queryset.filter(user=u) ## todo: combined another which shared option as an public
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


class ParseDeleteView(DeleteView):
    model = ParserConfigurationDef
    success_url = reverse_lazy('parser:parser_list')

    def get_context_data(self, **kwargs):
        context = super(ParseDeleteView, self).get_context_data(**kwargs)
        context['page_header'] = 'Parsers'
        context['cancel_url'] = reverse('parser:parser_list')
        return context

from .models import TextNotification
from .forms import TextNotificationForm


class BasePostIngestion(SingleObjectMixin, ModelFormSetView):
    factory_kwargs = {
        'can_delete': True,
        'extra': 3
    }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=ParserConfigurationDef.objects.all())
        return super(BasePostIngestion, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(parser=self.object)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a formset instance with the passed
        POST variables and then checked for validity.
        """
        self.object = self.get_object(queryset=ParserConfigurationDef.objects.all())
        self.object_list = self.get_queryset()
        formset = self.construct_formset()
        for form in formset.forms:
            form.instance.parser = self.object

        if formset.is_valid():
            return self.formset_valid(formset)
        else:
            return self.formset_invalid(formset)

    def get_context_data(self, **kwargs):
        context = super(BasePostIngestion, self).get_context_data(**kwargs)
        context['page_header'] = 'Parser'
        context['cancel_url'] = reverse('parser:parser_edit', args=[self.object.pk, ])
        return context


class MessageNotificationFormset(BasePostIngestion):
    template_name = 'parser_conf/post_parser_run_form.html'
    model = TextNotification
    form_class = TextNotificationForm

    def get_context_data(self, **kwargs):
        context = super(MessageNotificationFormset, self).get_context_data(**kwargs)
        context['widget_heading'] = 'Text Notifications'
        context['icon'] = format_html('<i class="fa fa-paper-plane"></i>')

        return context


class EmailNotificationFormset(BasePostIngestion):
    template_name = 'parser_conf/post_parser_run_form.html'
    model = EmailNotification
    form_class = EmailNotificationForm

    def get_context_data(self, **kwargs):
        context = super(EmailNotificationFormset, self).get_context_data(**kwargs)
        context['widget_heading'] = 'Email Notifications'
        context['icon'] = format_html('<i class="fa fa-envelope"></i>')

        return context

class ReportFormset(BasePostIngestion):
    template_name = 'parser_conf/post_parser_run_form.html'
    model = PostIngestionReport
    form_class = PostIngestionReportForm

    def get_context_data(self, **kwargs):
        context = super(ReportFormset, self).get_context_data(**kwargs)
        context['widget_heading'] = 'Reports '
        context['icon'] = format_html('<i class="fa fa-paperclip"></i>')
        return context
