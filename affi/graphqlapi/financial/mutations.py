import graphene
from graphql_jwt.decorators import login_required

from ...financial.models import Wallet

class UpdateWallet(graphene.Mutation):
    class Arguments:
        bank_account_number = graphene.String(required=True)
        bank_name = graphene.String()
        bank_account_name = graphene.String()
    
    status = graphene.String()
    error = graphene.String()

    @login_required
    def mutate(self, info, bank_account_number, bank_name, bank_account_name):
        user = info.context.user
        wallet = Wallet.objects.filter(user=user)
        if not wallet.exists():
            return UpdateWallet(status="Failed", error="There is no wallet for this user")
        wallet = wallet.first()
        wallet.bank_account_number = bank_account_number
        wallet.bank_name = bank_name
        wallet.bank_account_name = bank_account_name
        wallet.save()
        return UpdateWallet(status="success")



class FinancialMutation(graphene.ObjectType):
    update_wallet = UpdateWallet.Field()