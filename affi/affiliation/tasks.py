import requests

from woocommerce import API

from ..celery import app
from ..shop.models import Shop
from ..product.models import Product
from ..affiliation.models import Order

# @app.task
def get_products_by_order(shop_id, base_order_id, order_id):
    shop = Shop.objects.get(id=shop_id)
    wcapi = API(
        url=shop.url,  # Your store URL
        consumer_key=shop.api_cunsumer_key,  # Your consumer key
        consumer_secret=shop.api_secret_key,  # Your consumer secret
        wp_api=True,  # Enable the WP REST API integration
        version="wc/v3",  # WooCommerce WP REST API version
        timeout=10
    )
    try:
        data = wcapi.get(f"orders/{base_order_id}").json()
    except:
        return None
    status = data["status"]
    line_items = data["line_items"]
    products = [Product.objects.filter(base_id=product["product_id"]).first() for product in line_items]
    related_order = Order.objects.get(id=order_id)
    related_order.status = status
    related_order.related_products.add(*products)
    related_order.save()


    