import pytest
from ..models import OrderConfig
from .. import factories

pytestmark = pytest.mark.django_db

@pytest.fixture
def order_config():
    return factories.OrderConfigFactory(
        order_number_prefix="TEST-",    
        order_number_next=1 
    )

class TestOrderConfig:
    def test_order_config(self, order_config):
        assert OrderConfig.objects.get_next_number() == "TEST-1"
        assert OrderConfig.objects.get_next_number() == "TEST-2"
        assert OrderConfig.objects.get_next_number() == "TEST-3"
        
        order_config = OrderConfig.objects.get_order_config()
        assert order_config.order_number_next == 4
        
        
    def test_get_order_config(self, order_config):
        
        assert OrderConfig.objects.get_order_config() == order_config
        
        
        
    def test_get_next_number(self, order_config):
            
            assert OrderConfig.objects.get_next_number() == "TEST-1"
            assert OrderConfig.objects.get_next_number() == "TEST-2"