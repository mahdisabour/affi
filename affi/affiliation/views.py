import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Order
from ..shop.models import Shop

# @csrf_exempt
# @require_POST
# def woocommerce_update_order(request):
#     try:
#         data = json.loads(request.body)
#         header = request.META
#         shop_url = header["HTTP_X_WC_WEBHOOK_SOURCE"]
#         shop_objects = Shop.objects.get(url=shop_url) 
#         base_id = data["id"]
#         order_object = Order.objects.get()


        
#         return HttpResponse(status=200)

#     except Exception as e:
#         return HttpResponse(status=200)