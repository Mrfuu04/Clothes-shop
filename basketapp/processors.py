from basketapp.models import Basket


def basket(request):
    """Корзина доступна во всех шаблонах проекта"""
    basket_list = []
    if request.user.is_authenticated:
        basket_list = Basket.objects.filter(user=request.user.id).select_related()
    return {'basket': basket_list}