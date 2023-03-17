import base64


from rest_framework import serializers


from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),
                               name='temp.' + ext)
        return super().to_internal_value(data)


def delete_dub(list_product):
    j = 0
    try:
        while True:
            obr_ing = list_product[j][0].lower()
            obr_measure = list_product[j][2].lower()
            m = 0+j
            for i in range(1, len(list_product)):
                m += 1
                if (list_product[m][0].lower() == obr_ing
                        and list_product[m][2].lower() == obr_measure):
                    list_product[j][1] += list_product[m][1]
                    del (list_product[m])
                    m = 0+j
            j += 1
    except IndexError:
        return list_product
