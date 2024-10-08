from django.urls import path, include
from . import views

app_name = 'orders'


order_urlpatterns = [
     path("create-line-item/", views.CreateOrderLineItemView.as_view(), name="create_line_item"),
     path("update-line-item/<int:line_item_id>/", views.UpdateOrderLineItemView.as_view(), name="update_line_item"),
     path("delete-line-item/<int:line_item_id>/", views.RemoveOrderLineItemView.as_view(), name="delete_line_item"),
]

urlpatterns = [
    path("", views.OrderList.as_view(), name="list"),
    path("create/", views.CreateOrder.as_view(), name="create"),
    path("update/<int:pk>/", views.UpdateOrder.as_view(), name="update"),
    path("details/<int:pk>/", views.OrderDetailsView.as_view(), name="details"),
    path("line-items/<int:pk>/", views.OrderLineItemsView.as_view(), name="line_items"),
    path("update/customer/", views.CustomerOrderUpdateView.as_view(), name="update_customer"),
    path("order/<int:order_id>/", include(order_urlpatterns)),
]
