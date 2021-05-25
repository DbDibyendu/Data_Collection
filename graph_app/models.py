
from django.db import models

# Create your models here.


class InteractiveModels(models.Model):

    crypto = models.CharField(max_length=256, null=True)

    def __str__(self):
        return self.crypto


class StocksCompanyModels(models.Model):
    companycode = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.companycode