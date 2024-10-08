from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
from base.models import BaseModel
from django.db.transaction import atomic
from .managers import OrderConfigManager


#
#
# Order Configuration Model
# - Singleton model to store order configuration
#
#
class OrderConfig(BaseModel):
    objects = OrderConfigManager()

    class Meta:
        verbose_name = "Order Configuration"
        verbose_name_plural = "Order Configurations"

    order_number_prefix = models.CharField(max_length=255, blank=True)
    order_number_next = models.IntegerField(default=1)

    def __str__(self):
        return "Order Configuration"

    
    def clean(self):
        # validate singleton
        if OrderConfig.objects.exists() and self.pk != 1:
            raise ValidationError("There can only be one OrderConfig instance")
        
    # ensure I am a singleton object
    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


#
#
# Order Model
# - Represents an order
#
#
class Order(BaseModel):
    order_number = models.CharField(
        max_length=50, null=False, blank=True, unique=True, default=""
    )
    customer = models.ForeignKey("customers.Customer", on_delete=models.RESTRICT)
    
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    
    due_date = models.DateField()
    date_completed = models.DateField(null=True, blank=True)
    equipment_description = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    admin_password = models.CharField(max_length=255, blank=True)
    customer_po = models.CharField(max_length=255, blank=True)

    description_of_work = models.TextField(blank=False)
    work_performed = models.TextField(blank=True)

    def _build_order_number(self):
        if self.order_number:
            return

        self.order_number = OrderConfig.objects.get_next_number()

    @atomic
    def save(self, *args, **kwargs):
        self._build_order_number()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order# {self.order_number} :: {self.customer.name}"
    
    

class OrderLineItem(BaseModel):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="items")
    labor_item = models.ForeignKey("orders.LaborItem", on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=18, decimal_places=2, blank=False)
    description = models.CharField(max_length=255, blank=False)
    date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    finish_time = models.TimeField(blank=True, null=True)
    labor_rate = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=False, editable=False)
    
    def __str__(self):
        if not self.labor_item:
            return f"{self.quantity} {self.description}"
        
        return f"{self.labor_item} x {self.quantity} @ {self.labor_rate}"
    
    def total(self):
        if not self.labor_item:
            return 0
        
        return self.quantity * self.labor_rate
    
    def clean(self):
        if self.start_time and self.finish_time and self.start_time >= self.finish_time:
            raise ValidationError({"finish_time": "Finish time must be after start time."})
        
        if not self.labor_rate and self.labor_item:
            self.labor_rate = self.labor_item.labor_rate
        
        super().clean()
    
    
class LaborItem(BaseModel):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, unique=True)
    is_taxable = models.BooleanField(default=False)
    default_labor_description = models.CharField(max_length=255, blank=True)
    labor_rate = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=False)
    
    class Meta:
        ordering = ["name"]
        
        constraints = [
            models.UniqueConstraint(Lower("name"), name="unique_labor_item_name"),
        ]
        
    def _validate_name(self):
        if LaborItem.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            raise ValidationError({"name": "Labor item with this name already exists."})
        
    def clean(self):
        self._validate_name()
        super().clean()
        
    def __str__(self) -> str:
        return f"{self.name} ${self.labor_rate:.2f}/hr {'(taxable)' if self.is_taxable else ''}"