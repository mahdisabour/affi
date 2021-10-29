from django.utils import timezone

from django.contrib.auth.models import BaseUserManager

class TransactionManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results

    def affiliator_transactions(self, user_id, days, *args, **kwargs):
        affiliator_tranactions = self.get_queryset(*args, **kwargs).filter(
            related_order__related_affiliation__affiliator__user__id=user_id
        )
        affiliator_transaction_by_day = affiliator_tranactions.filter(
            updated_at__range=[
                timezone.now()-timezone.timedelta(days=days), timezone.now()]
        )
        return affiliator_transaction_by_day

    def shop_transactions(self, user_id, days, *args, **kwargs):
        shop_tranactions = self.get_queryset(*args, **kwargs).filter(
            related_order__related_affiliation__related_shop__user__id=user_id
        )
        shop_transaction_by_day = shop_tranactions.filter(
            updated_at__range=[
                timezone.now()-timezone.timedelta(days=days), timezone.now()]
        )
        return shop_transaction_by_day    
    
        
