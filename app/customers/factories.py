import factory
from . import models


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Customer
        
    name = factory.Faker('company')
    