from django.contrib import admin
from .models import InteractiveModels,StocksCompanyModels

# Register your models here.

admin.site.register(InteractiveModels)
admin.site.register(StocksCompanyModels)