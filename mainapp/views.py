import json
import os
from django.shortcuts import render
from datetime import datetime

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


def products(request, category_id=None):

    if category_id:
        products = Products.objects.filter(category=category_id)
    else:
        products = Products.objects.all()

    categories = ProductCategory.objects.all()

    content = {'title': 'GeekShop - Каталог',
               'categories': categories,
               'products': products,
               'time': now}

    return render(request, 'mainapp/products.html', content)

