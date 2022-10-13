from math import prod
from multiprocessing import context
from django.shortcuts import render
from . import services
import json
import re


def index(request, pk):
    products = services.drug_list()
    data = {}
    if request.POST:
        for key, value in request.POST.items():
            if not value in (0, '0') and key != "tg_user" and key != 'csrfmiddlewaretoken':
                data[key] = value
        product = services.order_create(request, data)
        all_sum = 0
        product_dict = {}
        for product1 in product.get('items'):
            all_sum += product1['medicine']['price'] * product1['number']
            product_dict[product1['medicine']['name']] = f"{product1['number']} x {product1['medicine']['price']}"
        context = {
            "all_sum": price_format(all_sum),
            "product_dict": product_dict,
            'product':product
        }
        return render(request, "chek.html", context)
    context = {
        "products": products,
        "tg_id": pk
    }
    return render(request, "index.html", context)

def price_format(inp):
    if inp:
        price = int(inp)
        res = "{:,}".format(price)
        formated = re.sub(",", " ", res)
        return formated
    else:
        return inp