import calendar
import datetime
import os

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings

from helpers import helpers
from core import models as core_models

logger = get_task_logger(__name__)

@shared_task
def generate_pdf(data_id: int):
    pass