from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView



class IndexView(TemplateView):
    template_name = 'index.html'