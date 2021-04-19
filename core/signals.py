from django.db.models.signals import post_save
from django.dispatch import receiver
from celery.utils.log import get_task_logger

from core import models as core_models
from core import tasks as core_tasks

logger = get_task_logger(__name__)


@receiver(post_save, sender=core_models.Data)
def single_to_create_pdf_of_the_data(sender, instance, **kwargs):
    if instance.status == "INIT":
        core_tasks.generate_pdf.delay(instance.pk)
        
