from django.contrib.auth.models import BaseUserManager

from ..affiliation.models import Order

class ShopManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results

