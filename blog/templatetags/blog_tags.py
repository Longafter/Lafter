# 创建了新的tags标签文件后必须重启服务器

from django import template
from ..models import Article, Category, Tag
from django.db.models.aggregates import Count
from django.utils.html import mark_safe
import re

register = template.Library()


# 文章相关的自定义模板标签函数
@register.simple_tag
def get_article_list(sort=None, num=None):
    '''获取指定排序方式和指定数量的文章'''
    if sort:
        if num:
            return Article.objects.order_by(sort)[:num]
        return Article.objects.order_by(sort)
    if num:
        return Article.objects.all()[:num]
    return Article.objects.all()


@register.simple_tag
def get_tag_list():
    '''返回标签列表'''
    return Tag.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)


@register.simple_tag
def get_category_list():
    '''返回分类列表'''
    return Category.objects.annotate(total_num=Count('article')).filter(total_num__gt=0)


@register.inclusion_tag('blog/tags/article_list.html')
def load_article_summary(article_list):
    '''返回文章列表模板'''
    return {'article_list': article_list}


@register.inclusion_tag('blog/tags/pagecut.html', takes_context=True)
def load_pages(context):
    '''分页标签模板，不需要传递参数，直接继承参数'''


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
