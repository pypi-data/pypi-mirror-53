from django.conf.urls import url
from oscar.apps.dashboard.reports import apps
from oscar.core.loading import get_class


class ReportsDashboardConfig(apps.ReportsDashboardConfig):
    name = 'oscarreports'


    def ready(self):
        super().ready()
        from . import handlers  # NOQA
        self.index_view = get_class('reports_dashboard.views', 'IndexView')


    def get_urls(self):
        urls = [
            url(r'^$', self.index_view.as_view(), name='reports-index'),
        ]
        return self.post_process_urls(urls)
