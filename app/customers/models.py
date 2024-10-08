from django.db import models
from base.models import BaseModel
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower
 

class Customer(BaseModel):
    
    class Meta:
        
        constraints = [
            models.UniqueConstraint(Lower("name"), name='unique_name'),
        ]
    
    name = models.CharField(max_length=255, db_index=True, unique=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
   
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
   
    def __str__(self):
        return f"{self.name} (id#{self.id})"
    
    def clean(self):
        self._validate_customer_name()
        super().clean()
        
    
    def _validate_customer_name(self):
        """ Ensure customer name is unqiue and display human error message"""
        if self.name and Customer.objects.exclude(pk=self.pk).filter(name__iexact=self.name).exists():
            raise ValidationError({"name": "Customer with this name already exists."})        
            
            
    def __str__(self):
        return self.name

