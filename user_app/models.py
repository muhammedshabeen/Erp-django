from django.db import models
from erp_app.models import UserModel, Project, MainTask, Task
from erp_app.utils import *
from datetime import timedelta, datetime

class Attendance(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateField()
    punch_in_time = models.TimeField(null=True, blank=True)
    lunch_in_time = models.TimeField(null=True, blank=True)
    lunch_out_time = models.TimeField(null=True, blank=True)
    punch_out_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    
    def total_work_time(self):
        if self.punch_in_time and self.punch_out_time:
            start = datetime.combine(self.date, self.punch_in_time)
            end = datetime.combine(self.date, self.punch_out_time)
            total_work = end - start

            if self.lunch_in_time and self.lunch_out_time:
                lunch_start = datetime.combine(self.date, self.lunch_in_time)
                lunch_end = datetime.combine(self.date, self.lunch_out_time)
                lunch_break = lunch_end - lunch_start
                total_work -= lunch_break

            return total_work
        return timedelta(0)
    

class TodayTask(BaseContent):
    date = models.DateField()
    project_name = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='today_project',limit_choices_to={'status':True})
    main_task = models.ForeignKey(MainTask,on_delete=models.CASCADE,limit_choices_to={'status':True})
    sub_task = models.ForeignKey(Task,on_delete=models.CASCADE,limit_choices_to={'status':True})
    time = models.TimeField()
    description = models.TextField()
    
