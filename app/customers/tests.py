import pytest
from .models import Customer    
from .factories import CustomerFactory  


pytestmark = pytest.mark.django_db


class TestCustomer:
    
    def test_customer(self):
         
         customer = CustomerFactory()
         assert customer
