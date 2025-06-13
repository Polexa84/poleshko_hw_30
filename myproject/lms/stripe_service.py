# stripe_service.py
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(name, description):
    """Создает продукт в Stripe."""
    try:
        product = stripe.Product.create(
            name=name,
            description=description,
        )
        return product
    except Exception as e:
        raise Exception(f"Ошибка при создании продукта Stripe: {e}")


def create_stripe_price(product_id, unit_amount, currency="usd"):
    """Создает цену в Stripe."""
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=unit_amount,  # Цена в центах
            currency=currency,
        )
        return price
    except Exception as e:
        raise Exception(f"Ошибка при создании цены Stripe: {e}")


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Создает сессию оформления заказа в Stripe."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return session
    except Exception as e:
        raise Exception(f"Ошибка при создании сессии Stripe: {e}")


def retrieve_stripe_checkout_session(session_id):
    """Получает информацию о сессии оформления заказа в Stripe."""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session
    except Exception as e:
        raise Exception(f"Ошибка при получении сессии Stripe: {e}")