# -*- coding: utf-8 -*-
import datetime
from contextlib import closing
from collections import OrderedDict
from pkgutil import iter_modules
from django.db import connection
from django.conf import settings
from novatio.base.utils.db_helpers import *
import re


def drug_list():
    try:
        with closing(connection.cursor()) as cursor:
            sql = f"""
                   select *
                   from tg_medicine
                   """
            cursor.execute(sql)
            items = dictfetchall(cursor)
        result = []
        if items:
            for item in items:
                result.append(OrderedDict([
                    ('id', item['id']),
                    ('name', item['name']),
                    ('code', item['code']),
                    ('price', item['price']),
                    ('sort', item['sort']),
                    ('category_id', item['category_id']),
                    ('old_price', item['old_price']),
                    ('created_at', item['created_at'])
                ]))
        else:
            result = None
    except Exception as e:
        print("error", e)
        result = None
    return OrderedDict([
        ('items', result)
    ])


def order_create(request, data):
    print(">>>>>", data)
    with closing(connection.cursor()) as cursor:
        sql = f"""INSERT INTO tg_order(status, created_at , user_id)
                VALUES (1,'{datetime.datetime.now()}', {request.POST.get('tg_user')})
                RETURNING id;
                """
        cursor.execute(sql)
        order_id = dictfetchone(cursor)
    for key, value in data.items():
        with closing(connection.cursor()) as cursor:
            sql = f"""INSERT INTO tg_productssold("number",created_at , medicine_id, user_id, order_id, price_product, is_active)
                    VALUES ({value},'{datetime.datetime.now()}', {key}, {request.POST.get('tg_user')}, {order_id.get('id')}, 
                    (select sum(tg_medicine.price)  from tg_medicine  where tg_medicine.id ={key}), true)
                    """
            cursor.execute(sql)

    with closing(connection.cursor()) as cursor:
        sql = f"""select tg_productssold.id ,tg_productssold.price_product, tg_productssold.order_id,tg_productssold."number",tg_productssold.created_at,(select row_to_json(qaz) from( select tg_medicine.id, tg_medicine.name, tg_medicine.price 
					from tg_medicine where tg_medicine.id=tg_productssold.medicine_id) qaz) as medicine,
                    (select array_agg(row_to_json(qaz))from( select tg_user.id, tg_user.first_name, tg_user.last_name, tg_user.phone_number, tg_user.tg_id 
                                    from tg_user where tg_user.id=tg_productssold.user_id) qaz) as tg_user
                from tg_productssold 
                where order_id = {order_id.get('id')}
                """
        cursor.execute(sql)
        items = dictfetchall(cursor)
    result = []
    if items:
        for item in items:
            result.append(OrderedDict([
                ('id', item['id']),
                ('price_product', item['price_product']),
                ('order_id', item['order_id']),
                ('medicine', item['medicine']),
                ('user', item['tg_user']),
                ('number', item['number']),
                ('created_at', item['created_at'].strftime('%d/%m/%y')),
            ]))
    else:
        result = None
    return OrderedDict([
        ('items', result)
    ])