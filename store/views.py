import os

import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from dotenv import load_dotenv

from .models import Discount, Item, Order, Tax

load_dotenv()
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

stripe.api_key = STRIPE_SECRET_KEY

class ItemsShow(ListView):
    model = Item
    template_name = 'items.html'
    paginate_by = 100

class ItemDetailView(TemplateView):
    template_name = 'item_detail.html'

    def get_context_data(self, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['id'])
        context = super().get_context_data(**kwargs)
        context['item'] = item
        context['stripe_publishable_key'] = STRIPE_PUBLISHABLE_KEY
        return context

@csrf_exempt
def order_detail(request):
    order = Order.objects.first()
    stripe_publishable_key = STRIPE_PUBLISHABLE_KEY
    return render(request, 'order_detail.html', {
        'order': order,
        'stripe_publishable_key': stripe_publishable_key,
    })

@csrf_exempt
def add_item_to_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order = Order.objects.first()
    order.items.add(item)
    return render(request, 'item_detail.html', {'item': item})

@csrf_exempt
def remove_item_from_order(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order = Order.objects.first()
    order.items.remove(item)
    return render(request, 'item_detail.html', {'item': item})

@csrf_exempt
def buy_order(request):
    order = Order.objects.first()

    try:
        discount = order.discount
    except Discount.DoesNotExist:
        discount = None
    try:
        tax = order.tax
    except Tax.DoesNotExist:
        tax = None

    total_cost = order.get_total_cost()
    if discount:
        total_cost -= discount.amount
    if tax:
        total_cost += tax.amount

    line_items = [{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Заказ',
                },
                'unit_amount': int(float(total_cost) * 100),
            },
            'quantity': 1,
    }]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(order.get_absolute_url()),
        cancel_url=request.build_absolute_uri(order.get_absolute_url()),
    )
    return JsonResponse({'session_id': session.id})

@csrf_exempt
def get_checkout_session(request, id):
    item = get_object_or_404(Item, pk=id)

    line_items = [{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.name,
            },
            'unit_amount': int(item.price * 100),
        },
        'quantity': 1,
    }]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(item.get_absolute_url()),
        cancel_url=request.build_absolute_uri(item.get_absolute_url()),
    )

    return JsonResponse({'session_id': session.id})
