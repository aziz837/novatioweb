import json
import requests
from text_unidecode import unidecode
from django.utils.text import slugify
from datetime import datetime


def send_code_sms(phone, code):
    headers = {'content-type': 'multipart/form-data;'}
    login = 'chinoztaxi'
    password = 'chin@zTa@xi2022'
    url = "https://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s" % (login, password, phone, code)

    try:
        r = requests.post(url, headers=headers)
        content = r.content
        if content:
            try:
                response = json.loads(content.decode("utf-8"))
            except ValueError:
                response = content
        else:
            response = content

        return r.status_code, response

    except Exception as e:
        print("sent error: ~ %s" % e)
        return 0


def create_alias(instance):
    alias = instance.alias
    if alias is None or alias == "":
        alias = slugify(unidecode(instance.name))
    Klass = instance.__class__
    if instance.pk:
        qs_exists = Klass.objects.filter(alias=alias).exclude(id=instance.pk).exists()
    else:
        qs_exists = Klass.objects.filter(alias=alias).exists()

    if qs_exists:
        alias = slugify("{}-{}".format(unidecode(instance.name), datetime.now().timestamp()))

    return alias
