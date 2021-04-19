from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Data(models.Model):
    STATUS_CHOICES = [
        ('INIT', 'Initiated'),
        ('PROG', 'On Progress'),
        ('FINI', 'Finished'),
        ('FAIL', 'Failed')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    data = models.JSONField()
    image = models.ImageField(upload_to="static/uploads/images", null=False, blank=False)
    generated_pdf = models.FileField(upload_to="static/uploads/pdfs", null=True, blank=True)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, default='INIT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Data"
    
    def __str__(self):
        return "{} {} [{}]".format(self.user.first_name, self.user.last_name, str(self.pk))

