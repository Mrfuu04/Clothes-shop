import json
import os

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from datetime import datetime

from django.views.generic import DetailView

from mainapp.models import Products, ProductCategory

now = datetime.today().strftime('%H:%M')
# Create your views here.
MODULE_DIR = os.path.dirname(__file__)

def read_json(file):
    file_path = os.path.join(MODULE_DIR, file)
    return json.load(open(file_path, encoding='utf-8'))


def index(request):
    content = {'title': 'GeekShop',
               'time': now}

    return render(request, 'mainapp/index.html', content)


def products(request, category_id=None, page=1):

    if category_id:
        products = Products.objects.filter(category=category_id)
    else:
        products = Products.objects.all()

    pagination = Paginator(products, per_page=3)
    try:
        product_pagination = pagination.page(page)
    except PageNotAnInteger:
        product_pagination = pagination.page(1)
    except EmptyPage:
        product_pagination = pagination.page(pagination.num_pages)


    categories = ProductCategory.objects.all()

    content = {'title': 'GeekShop - Каталог',
               'categories': categories,
               'products': product_pagination,
               'time': now}

    return render(request, 'mainapp/products.html', content)


class ProductDetail(DetailView):
    model = Products
    template_name = 'mainapp/product_detail.html'
