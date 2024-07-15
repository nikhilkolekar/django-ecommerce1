from django.shortcuts import render, redirect
from .models import Order, OrderItem
from apps.products.models import Product

def order_summary(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    return render(request, 'orders/order_summary.html', {'order': order})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    return redirect('order_summary')

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Order
from .forms import PaymentForm

def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
            token = form.cleaned_data['stripe_token']
            order = Order.objects.filter(user=request.user, is_paid=False).first()
            amount = int(order.total_cost() * 100)  # Convert to cents
            try:
                charge = stripe.Charge.create(
                    amount=amount,
                    currency='usd',
                    description='E-commerce order',
                    source=token,
                )
                order.is_paid = True
                order.save()
                return redirect('order_complete')
            except stripe.error.StripeError:
                # Handle error
                pass
    else:
        form = PaymentForm()
    return render(request, 'orders/payment.html', {'form': form})
