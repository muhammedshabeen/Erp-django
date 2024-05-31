from django.db import models


class BaseContent(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(default='Active',max_length=20,choices=(
        ('Active','Active'),
        ('Inactive','Inactive'),
    ))