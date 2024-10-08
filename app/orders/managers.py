from django.db import models
from django.core.exceptions import ValidationError


class OrderConfigManager(models.Manager):
    def get_order_config(self):
        if config := self.select_for_update().first():
            return config
        
        raise ValidationError("No Order Configuration exists, please create Order Configuration")


    def get_next_number(self):
        order_config = self.get_order_config()
        order_number = f"{order_config.order_number_prefix}{order_config.order_number_next}"
        order_config.order_number_next += 1
        order_config.save()
        return order_number
    