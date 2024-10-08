from django import forms
from django.urls import reverse_lazy
from base.forms import DaisyFormHelper
from . import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = "__all__"
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "date_completed": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        helper = DaisyFormHelper(self)

        self.fields["customer"].widget.attrs.update(
            {
                "hx-trigger": "change",
                "hx-select": "#email_phone",
                "hx-target": "#email_phone",
                "hx-post": reverse_lazy("orders:update_customer"),
            }
        )

        self.fields["equipment_description"].widget.attrs.update({"rows": 3})
        self.fields["description_of_work"].widget.attrs.update({"rows": 3})
        self.fields["work_performed"].widget.attrs.update({"rows": 3})

        helper.add_class("customer", "font-semibold")

        self.fields["phone"].widget.attrs.update({"placeholder": "Phone", 'class': 'input input-bordered'})
        self.fields['phone'].label = False
        
        self.fields["email"].widget.attrs.update({"placeholder": "Email", 'class': 'input input-bordered'})
        self.fields['email'].label = False
        

class OrderLineItemForm(forms.ModelForm):
    class Meta:
        model = models.OrderLineItem
        fields = ("quantity", "labor_item", "description", "date", "start_time", "finish_time") 
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "finish_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, order, **kwargs):
        self.order = order
        super().__init__(*args, **kwargs)

        helper = DaisyFormHelper(self)

        helper.add_class("labor_item", "font-semibold")
        
        self.fields["quantity"].widget.attrs.update({'autofocus': True})
        
    def save(self, commit=True):
        self.instance.order = self.order
        
        return super().save(commit=commit)