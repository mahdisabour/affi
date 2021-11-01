import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Product
from ..shop.models import Shop

@csrf_exempt
@require_POST
def woocommerce_update_product(request):
    try:
        data = json.loads(request.body)
        header = request.META
        shop_url = header["x-wc-webhook-source"]
        shop_objects = Shop.objects.get(url=shop_url)

        base_id = data["id"]
        price = data["price"]
        stock_status = data["stock_status"]
        
        product_object = Product.objects.get(base_id=base_id, related_shop=shop_objects)
        product_object.price = price 
        product_object.stock_status = stock_status
        product_object.save()
        

    except Exception as e:
        print(e)
        return HttpResponse(status=200)