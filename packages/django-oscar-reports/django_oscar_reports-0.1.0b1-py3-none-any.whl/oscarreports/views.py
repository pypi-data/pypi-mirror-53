from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableView
from psycopg2.extras import DateTimeTZRange
from .models import Report
from .tables import ReportTable
from .forms import ReportForm


class IndexView(FormMixin, SingleTableView):
    template_name = 'oscar/dashboard/reports/index.html'
    table_pagination = True
    model = Report
    table_class = ReportTable
    context_table_name = 'reports'
    desc_template = ''
    description = ''

    form_class = ReportForm

    def dispatch(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)
        return super().dispatch(request, *args, **kwargs)


    def get_queryset(self):
        queryset = self.model.objects.all().order_by('-created_on')
        return queryset


    def post(self, request, *args, **kwargs):
        if self.form.is_valid():
            # Create report
            report = Report()
            report.content_type = None
            report.owner = request.user
            report.type_code = self.form.cleaned_data['report_type']
            report.date_range = DateTimeTZRange(
                lower=self.form.cleaned_data['date_from'],
                upper=self.form.cleaned_data['date_to'])
            report.save()
            # Queue report
            report.queue()
            # Message user
            messages.info(request, _("Successfully queued report for generation"))
            return redirect('dashboard:reports-index')
        return self.get(request, *args, **kwargs)


    def get_table(self, **kwargs):
        table = super().get_table(**kwargs)
        table.caption = _("Reports")
        return table


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        return context
