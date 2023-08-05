# DynamicFieldSerializer for DRF


## Requirements

* Python (3.6, 3.7)
* Django (1.11, 2.0, 2.1, 2.2)
* Django Rest Framework >= 3.8.2

## Installation

Install using `pip`...

    pip install drf-dynamicfieldserializer

## How to use

```python

# models
class Profile(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    active = models.BooleanField(default=True)




# serializers.py
from rest_framework import serializers
from dynamicfield_serializer import DynamicFieldSerializer
from .models import Profile


class ProfileModelSerializer(DynamicFieldSerializer, ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"



#views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer


class ProfileAPIView(APIView):
    def get(self, request):
        response_fields = request.GET.get("response_fields","")
        if response_fields:
            response_fields = response_fields.split(",")
        qs = Profile.objects.all()
        data = ProfileSerializer(qs, response_fields=response_fields, many=True).data
        return Response(data)
```

# Full response:
```
    $ curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/profiles/
    [
        {
            "id": 1,
            "name": "test",
            "email": "test@mail.ru",
            "phone": "+777777777",
            "active": true
        }
    ]
```

# Response with response_fields:
```
    $ curl -H 'Accept: application/json; indent=4' http://127.0.0.1:8000/profiles/?response_fields=phone,email
    [
        {
            "phone": "+777777777",
            "email": "test@mail.ru"
        }
    ]
```
