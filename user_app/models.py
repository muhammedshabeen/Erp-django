from django.db import models
from erp_app.models import UserModel

class Attendance(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField()
    punch_in_time = models.TimeField(null=True, blank=True)
    lunch_in_time = models.TimeField(null=True, blank=True)
    lunch_out_time = models.TimeField(null=True, blank=True)
    punch_out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
