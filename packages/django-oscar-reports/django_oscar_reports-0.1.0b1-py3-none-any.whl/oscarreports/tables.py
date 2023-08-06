from django.utils.translation import gettext_lazy as _
from django_tables2 import Column, TemplateColumn
from oscar.core.loading import get_class

DashboardTable = get_class('dashboard.tables', 'DashboardTable')


class ReportTable(DashboardTable):
    description = Column(accessor='description', orderable=False)
    date_range = TemplateColumn(
        template_name='oscar/dashboard/reports/report_row_date_range.html',
        verbose_name=_("Date Range"),
        orderable=False)

    owner = Column(accessor='owner.get_full_name', orderable=False, verbose_name=_('Owner'))
    status = Column(accessor='status_name', orderable=False, verbose_name=_('Status'))

    created_on = Column(accessor='created_on')
    queued_on = Column(accessor='queued_on')
    started_on = Column(accessor='started_on')
    completed_on = Column(accessor='completed_on')

    actions = TemplateColumn(
        template_name='oscar/dashboard/reports/report_row_actions.html',
        verbose_name=' ',
        orderable=False)

    class Meta(DashboardTable.Meta):
        pass
