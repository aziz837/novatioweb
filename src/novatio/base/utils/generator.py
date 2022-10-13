import random
import string
from contextlib import closing
from django.db import connection


SHORTCODE_MIN = 5


def code_generator(size=SHORTCODE_MIN, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_tabid(size=SHORTCODE_MIN):
    new_code = code_generator(size=size)
    extra_sql = """select(EXISTS(SELECT 1 FROM dav_drivers WHERE tab_id=%s)) as has"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(extra_sql, [new_code])
        exists = cursor.fetchone()
    if exists[0]:
        return create_tabid(size=size)
    return new_code
