from django.shortcuts import render, redirect, reverse, get_object_or_404
from decimal import Decimal
from django.conf import settings
import stripe
from orders.models import Order


# Создаем экземпляр Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))
        
        # Данные сеанса оформления платежа Stripe
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # Добавить позиции заказа в сеанс оформления платежа Stripe
        for item in order.items.all():
            session_data['line_items'].append({
                # Информация связанная с ценой
                'price_data': {
                    # Сумма в копейках
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'usd',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })

        # Создать сеанс для оформления платежа Stripe
        session = stripe.checkout.Session.create(**session_data)

        # Перенаправить к платежной форме Stripe
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html' , locals())
    

def payment_completed(request):
    return render(request, 'payment/completed.html')


def payment_canceled(request):
    return render(request, 'payment/canceled.html')


