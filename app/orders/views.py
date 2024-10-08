from django.shortcuts import render
from django.views.generic import ListView, View, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django_htmx.http import trigger_client_event
from django.http import HttpResponse
from django.utils import timezone
from django.urls import reverse_lazy
from . import models
from customers.models import Customer
from . import forms

def close_modal_and_refresh_items(request):
    res = HttpResponse()
    res.headers['HX-Trigger'] = 'order:itemsUpdated,modalSlide:close'
    return res
             


class OrderList(LoginRequiredMixin, ListView):
    context_object_name = "orders"
    template_name = "orders/order_list.html"
    model = models.Order
    paginate_by = 25
    ordering = "id"


class CreateOrder(LoginRequiredMixin, CreateView):
    form_class = forms.OrderForm
    template_name = "orders/order_create.html"
    
    def get_success_url(self):
        return reverse_lazy("orders:details", kwargs={"pk": self.object.pk})


class UpdateOrder(LoginRequiredMixin, UpdateView):
    form_class = forms.OrderForm
    model = models.Order
    template_name = "orders/order_edit.html"
    
    def get_success_url(self):
        return reverse_lazy("orders:details", kwargs={"pk": self.object.pk})


class CustomerOrderUpdateView(LoginRequiredMixin, View):
    """
    This view is used to update the email and phone fields in the order form
    when a customer is selected.
    """
    template_name = "orders/_fields_from_customer.html"

    def post(self, request):
        customer_id = request.POST.get("customer", None)
        initials={}
        if customer_id:
            try:
                customer = Customer.objects.get(pk=customer_id)
                initials["address"] = customer.address
                initials["city"] = customer.city
                initials["state"] = customer.state
                initials["zip"] = customer.zip
                initials["phone"] = customer.phone
                initials["email"] = customer.email
            except Customer.DoesNotExist:
                pass

        form = forms.OrderForm(initial=initials)
        return render(request, self.template_name, {'form': form})



class OrderDetailsView(LoginRequiredMixin, View):
    template_name = "orders/order_details.html"

    def get(self, request, pk):
        order = models.Order.objects.get(pk=pk)
        return render(request, self.template_name, {"order": order})
    
    
class OrderLineItemsView(LoginRequiredMixin, View):
    template_name = "orders/order_line_items.html"

    def get(self, request, pk):
        order = models.Order.objects.get(pk=pk)
        return render(request, self.template_name, {"order": order})
    
    
class CreateOrderLineItemView(LoginRequiredMixin, View):
     
    template_name = "orders/_line_item_form.html"
    
    def get(self, request, order_id):
        order = models.Order.objects.get(pk=order_id)
        form = forms.OrderLineItemForm(order=order, initial={"date": timezone.now().date()})
        context = { 'form': form, 'order': order }
        return render(request, self.template_name, context)
        
    def post(self, request, order_id):
        order = models.Order.objects.get(pk=order_id)
        form = forms.OrderLineItemForm(request.POST, order=order)
        if form.is_valid():
            form.save()
            return close_modal_and_refresh_items(request)

        return render(request, self.template_name, {'form': form, 'order': order})

class UpdateOrderLineItemView(LoginRequiredMixin, View):
     
    template_name = "orders/_line_item_form.html"
    
    def get(self, request, order_id, line_item_id):
        order = models.Order.objects.get(pk=order_id)
        line_item = order.items.get(pk=line_item_id)
        form = forms.OrderLineItemForm(instance=line_item, order=order, initial={"date": timezone.now().date()})
        context = { 'form': form, 'order': order }
        return render(request, self.template_name, context)
        
    def post(self, request, order_id, line_item_id):
        order = models.Order.objects.get(pk=order_id)
        line_item = order.items.get(pk=line_item_id)
        form = forms.OrderLineItemForm(request.POST, instance=line_item, order=order)
        if form.is_valid():
            form.save()
            return close_modal_and_refresh_items(request)
        context = { 'form': form, 'order': order }
        return render(request, self.template_name, context)


class RemoveOrderLineItemView(LoginRequiredMixin, View):
    def delete(self, request, order_id, line_item_id):
        order = models.Order.objects.get(pk=order_id)
        line_item = order.items.get(pk=line_item_id)
        line_item.delete()
        return close_modal_and_refresh_items(request)