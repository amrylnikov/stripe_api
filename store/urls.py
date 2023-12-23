from django.urls import path

from .views import (ItemDetailView, ItemsShow, add_item_to_order, buy_order,
                    get_checkout_session, order_detail, remove_item_from_order)

urlpatterns = [
    path('', ItemsShow.as_view(), name='items_show'),
    path('item/<int:id>/', ItemDetailView.as_view(), name='item_detail'),
    path('order/', order_detail, name='order_detail'),
    path('add-to-order/<int:item_id>/', add_item_to_order, name='add_item_to_order'),
    path('remove-from-order/<int:item_id>/', remove_item_from_order, name='remove_item_from_order'),
    path('buy-order/', buy_order, name='buy_order'),
    path('buy/<int:id>/', get_checkout_session, name='get_checkout_session'),
]
