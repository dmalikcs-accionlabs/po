import django.views.static
import django.views.generic
from django.urls import path, include, \
    re_path
from django.contrib import admin
from django.conf import settings
from .views import IndexView, IngestionReplicationView, \
    EmailIngestionAPI

class SettingsTemplateView(django.views.generic.TemplateView):
    def get_context_data(self, **kwargs):
        context = super(SettingsTemplateView, self).get_context_data(**kwargs)
        context['settings'] = settings
        return context

from ingestion.views import InventoryListAPIView


api_patterns = [
    path('inventory/', InventoryListAPIView.as_view()),
    path('ingestion/', EmailIngestionAPI.as_view()),
    ]


urlpatterns = [
    path('robots.txt', SettingsTemplateView.as_view(
        template_name='robots.txt', content_type='text/plain'
    )),
    path('', IndexView.as_view(), name="home"),
    path('api/', include(api_patterns)),
    path('admin/', admin.site.urls),
    path('users/', include(('users.urls', 'user'), namespace='user'), ),
    path('client/', include(('clients.urls', 'clients'), namespace='clients'), ),
    path('ingestion/', include(('ingestion.urls', 'ingestion'), namespace='ingestion'),),
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard'),),
    path('parser/', include(('parser_conf.urls', 'parser'), namespace='parser'),),
    path('upload/', IngestionReplicationView.as_view(), name="upload"),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        re_path('media/(?P<path>.*)', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
        path('__debug__/', include(debug_toolbar.urls)),
    ]