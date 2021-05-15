
from rest_framework import serializers 


from .models import InteractiveModels,StocksCompanyModels

class InteractiveSerializer(serializers.ModelSerializer):
    class Meta:

        model = InteractiveModels
        fields =  ["crypto"]

class StocksCompanySerializer(serializers.ModelSerializer):
    class Meta:

        model = StocksCompanyModels
        fields =  ["companycode"]