import pytest
from ..models import Order
from ..factories import OrderFactory, OrderConfigFactory

pytestmark = pytest.mark.django_db
 
@pytest.fixture 
def config():
    return OrderConfigFactory()
    
class TestOrder:
    
    def test_order(self, config):
        
        order = OrderFactory()
        assert order
        assert order.customer
        assert order.order_number
        assert order.due_date
        
        