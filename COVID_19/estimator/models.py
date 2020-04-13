from django.db import models

# Create your models here

class Log(models.Model):
    request_method = models.CharField(max_length=4)
    path = models.CharField(max_length=200)
    status_code = models.IntegerField(default=200)
    response_time = models.IntegerField(default=0)
    time_unit = models.CharField(max_length=2)

    def __str__(self):
        return self.request_method


