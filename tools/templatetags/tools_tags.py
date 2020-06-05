# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import FriendLink, Activate
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
import re

register = template.Library()


@register.simple_tag
def get_star(num):
    '''得到一排星星'''
    tag_i = '<i class="fa fa-star"></i>'
    return mark_safe(tag_i * num)


@register.simple_tag
def get_star_title(num):
    '''得到星星个数的说明'''
    the_dict = {
        1: '【1颗星】：微更新，涉及轻微调整或者后期规划了内容',
        2: '【2颗星】：小更新，小幅度调整，一般不会迁移表格',
        3: '【3颗星】：中等更新，一般会增加或减少模块，有表格的迁移',
        4: '【4颗星】：大更新，涉及到应用的增减',
        5: '【5颗星】：最大程度更新，一般涉及多个应用和表格的变动',
    }
    return the_dict[num]


@register.simple_tag
def my_highlight(text, q):
    '''自定义标题搜索词高亮函数，忽略大小写'''
    if len(q) > 1:
        try:
            text = re.sub(q, lambda a: '<span class="highlighted">{}</span>'.format(a.group()),
                          text, flags=re.IGNORECASE)
            text = mark_safe(text)
        except:
            pass
    return text


@register.simple_tag
def get_request_param(request, param, default=None):
    '''获取请求的参数'''
    return request.POST.get(param) or request.GET.get(param, default)


@register.simple_tag
def get_friends():
    '''获取活跃的友情链接'''
    return FriendLink.objects.filter(is_show=True, is_active=True)


@register.simple_tag
def get_activates():
    '''获取活跃的友情链接'''
    return Activate.objects.filter(is_active=True)
