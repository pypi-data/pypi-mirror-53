import logging
import sys

from celery import shared_task
from .models import Report, ReportSchedule


logger = logging.getLogger(__name__)


@shared_task(ignore_result=True, bind=True, default_retry_delay=1 * 60)
def generate_document(self, report_id):
    """
    Generates the report document. Retry after 1 minute
    """

    try:
        report = Report.objects.get(pk=report_id)
    except Report.DoesNotExist as exc:
        raise self.retry(exc=exc, max_retries=3)
    try:
        report.generate_document()
    except Exception as exc:
        msg = "Error generating report"
        logger.error(msg, exc_info=sys.exc_info())
        raise self.retry(exc=exc)


@shared_task(ignore_result=True)
def schedule_task(report_schedule_id):
    report_schedule = ReportSchedule.objects.get(pk=report_schedule_id)
    report_schedule.schedule_report()
