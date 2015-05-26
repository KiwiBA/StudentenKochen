from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
            return self.name
        