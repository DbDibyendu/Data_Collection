 
from django.db import models

# Create your models here.



class InteractiveModels(models.Model):

    crypto = models.CharField(max_length = 256,null=True)
    def __str__(self):
        return self.companycode 