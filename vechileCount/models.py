from django.db import models

class statuscount(models.Model):
    Date = models.DateField()
    Time = models.TimeField()
    count = models.IntegerField()
    Status = models.CharField(max_length=80)
    