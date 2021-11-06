import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Product
from ..shop.models import Shop
from ..shop.tasks import WooCommerceHandler

@csrf_exempt
@require_POST
def woocommerce_update_product(request):
    try:
        data = json.loads(request.body)
        header = request.META
        shop_url = header["HTTP_X_WC_WEBHOOK_SOURCE"]
        shop_objects = Shop.objects.get(url=shop_url)

        base_id = data["id"]
        price = data["price"]
        stock_status = data["stock_status"]
        
        product_object = Product.objects.get(base_id=base_id, related_shop=shop_objects)
        product_object.price = price 
        product_object.stock_status = stock_status
        product_object.save()
        return HttpResponse(status=200)

    except Exception as e:
        print(e)
        return HttpResponse(status=200)


@csrf_exempt
@require_POST
def woocommerce_create_product(request):
    try:
        data = json.loads(request.body)
        header = request.META
        shop_url = header["HTTP_X_WC_WEBHOOK_SOURCE"]
        shop_objects = Shop.objects.get(url=shop_url)

        woocommerce_handler = WooCommerceHandler(shop=shop_objects)
        woocommerce_handler.get_products(products=list(data))
        
        return HttpResponse(status=200)

    except Exception as e:
        print(e)
        return HttpResponse(status=200)
