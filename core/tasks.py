import calendar
import datetime
import os
import pdfkit
import base64
from django.template.loader import get_template
from datetime import datetime
from django.conf import settings
from io import StringIO

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from core import models as core_models
from django.core.files import File

logger = get_task_logger(__name__)

@shared_task
def generate_pdf(data_id: int):
    data_obj = core_models.Data.objects.get(pk=data_id)
    data_obj.status = 'PROG'
    data_obj.save()

    pdf_file_name = None
    pdf_location = None
    
    try:
        time = datetime.now()

        image_path = os.path.join(settings.BASE_DIR, str(data_obj.image))

        # with open(image_path, "rb") as image_file:
        #     encoded_string = base64.b64encode(image_file.read())

        context = {
            "image": image_path,
            "data": data_obj.data
        }

        # logger.info(encoded_string)

        template = get_template("pdfTemplate.html")
        html_content = template.render(context)

        pdf_file_name = '{}_{}.pdf'.format(data_obj.created_at, str(data_id))
        pdf_location =  os.path.join(os.path.join(settings.BASE_DIR, 'generated_files'), pdf_file_name)

        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': 'utf-8',
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'enable-local-file-access': None
        }
        pdfkit.from_string(html_content, pdf_location, options=options)

        pdf_file = open(pdf_location, "rb")
        data_obj.generated_pdf.save(pdf_file_name, File(pdf_file))
        
        data_obj.status = 'FINI'
        data_obj.save()

    except:
        if pdf_location is not None:
            pdf_file = open(pdf_location, "rb")
            data_obj.generated_pdf.save(pdf_file_name, File(pdf_file), save=True)
            data_obj.status = 'FINI'
            data_obj.save()
        else:
            data_obj.status = 'FAIL'
            data_obj.save()