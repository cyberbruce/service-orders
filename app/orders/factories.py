import factory
from . import models


class OrderConfigFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.OrderConfig

    order_number_prefix = "TEST-"
    order_number_next = 1
    
    
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Order

    due_date = factory.Faker('date_this_year')
    customer = factory.SubFactory('customers.factories.CustomerFactory')
    