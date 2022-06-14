import json
import os

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from datetime import datetime

from mainapp.cache_functions import get_links_menu, get_links_menu_category
from mainapp.models import Products, ProductCategory
from django.views.generic import DetailView, ListView, DeleteView, UpdateView, CreateView, TemplateView

now = datetime.today().strftime('%H:%M')
# Create your views here.
MODULE_DIR = os.path.dirname(__file__)


def read_json(file):
    file_path = os.path.join(MODULE_DIR, file)
    return json.load(open(file_path, encoding='utf-8'))


class IndexView(TemplateView):
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'GeekShop'
        context['time'] = now
        return context


# def index(request):
#     content = {'title': 'GeekShop',
#                'time': now}
#
#     return render(request, 'mainapp/index.html', content)

class ProductsView(ListView):
    paginate_by = 3
    model = Products
    template_name = 'mainapp/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        if self.kwargs.get('cat_slug'):
            return get_links_menu_category(self.kwargs.get('cat_slug'))
            # return qs.filter(category=self.kwargs.get('category')).select_related('category')
        return get_links_menu()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = now
        context['title'] = 'GeekShop - Каталог'

        return context


# def products(request, category_id=None, page=1):
#
#     if category_id:
#         products = Products.objects.filter(category=category_id)
#     else:
#         products = Products.objects.all()
#
#     pagination = Paginator(products, per_page=3)
#     try:
#         product_pagination = pagination.page(page)
#     except PageNotAnInteger:
#         product_pagination = pagination.page(1)
#     except EmptyPage:
#         product_pagination = pagination.page(pagination.num_pages)
#
#
#     categories = ProductCategory.objects.all()
#
#     content = {'title': 'GeekShop - Каталог',
#                'categories': categories,
#                'products': product_pagination,
#                'time': now}
#
#     return render(request, 'mainapp/products.html', content)


class ProductDetail(DetailView):
    model = Products
    template_name = 'mainapp/product_detail.html'

