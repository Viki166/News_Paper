from django import template
from ..templatetags.profanity_list import profanity_list
import re
# В файле profanity_list  хранится список нежелательных слов
register = template.Library()

# Фильтр censor
@register.filter(name='censor')
def censor(value, arg='*'):
    list_value = re.split(r'\W+', value) # создаем из строки список слов, который нужно будет проверить на цензуру
    for word in list_value:
        if word.lower() in profanity_list: # сравниваем каждое слово со списком нежелательных слов
            list_value[list_value.index(word)] = arg # если находится плохое слово, заменяем его значением,заданным в arg
        else:
            word
    return ' '.join(list_value) # возвращаем отредактированную строку




