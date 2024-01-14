from django.db import models

# Create your models here.
class Tasks(models.Model):
    username = models.CharField(max_length=120)
    task_name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name
    