from django.http import JsonResponse
from django.views.generic.edit import FormView, FormMixin
from django.views.generic import View
from .forms import EventNameSearchForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .queries import ProductionIdQuery

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        print(form.errors)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        print(form.cleaned_data)
        venue_name = form.cleaned_data.get('venue_name')
        event_date = form.cleaned_data.get('event_date')
        event_time = form.cleaned_data.get('event_time')
        # p = ProductionIdQuery()
        # p.get_production_id(venue_name, event_date, event_time)
        # events = p.events
        if self.request.is_ajax():
            data = {'data': [{'production_id': 1234}, {'production_id': 3234}] or []}
            return JsonResponse(data)
        else:
            return ''


class ProductionSearchAPIView(AjaxableResponseMixin, FormMixin, View):
    form_class = EventNameSearchForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ProductionSearchAPIView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print(request.GET)
        form = self.form_class(request.GET)
        if form.is_valid():
            print("form is valid")
            return self.form_valid(form=form)
        else:
            print("form is invalid")
            return self.form_invalid(form=form)
