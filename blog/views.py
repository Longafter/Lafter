import markdown
import time, datetime
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.cache import cache
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension  # 锚点的拓展

from .models import Article, Tag, Category


class IndexView(ListView):
    """
        首页视图,继承自ListVIew，用于展示从数据库中获取的文章列表
    """
    # 获取数据库中的文章列表
    model = Article
    # template_name属性用于指定使用哪个模板进行渲染
    template_name = 'blog/index.html'
    # context_object_name属性用于给上下文变量取名（在模板中使用该名字）
    context_object_name = 'article_list'

    def get_ordering(self):
        ordering = super().get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering


class ArchiveView(ListView):
    model = Article
    template_name = 'blog/archive.html'
    context_object_name = 'article_list'
    paginate_by = 200
    paginate_orphans = 50


def AboutView(request):
    site_date = datetime.datetime.strptime('2020-05-30','%Y-%m-%d')
    return render(request, 'blog/about.html',context={'site_date':site_date})


class CategoryView(ListView):
    model = Article
    template_name = 'blog/category.html'
    context_object_name = 'article_list'

    def get_ordering(self):
        ordering = super().get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    # 重写通用视图的get_queryset方法，获取定制数据
    # 该方法默认获取指定模型的全部列表数据
    def get_queryset(self):
        queryset = super().get_queryset()
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return queryset.filter(category=cate)

    # 重写通用视图的get_context_data方法，获取定制模板变量字典
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cate = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context['search_tag'] = '文章分类'
        context['search_instance'] = cate
        return context


class TagView(ListView):
    model = Article
    template_name = 'blog/tag.html'
    context_object_name = 'article_list'

    def get_ordering(self):
        ordering = super().get_ordering()
        sort = self.kwargs.get('sort')
        if sort == 'v':
            return ('-views', '-update_date', '-id')
        return ordering

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        return queryset.filter(tags=tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, slug=self.kwargs.get('slug'))
        context['search_tag'] = '文章标签'
        context['search_instance'] = tag
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get_object(self):
        obj = super().get_object()
        # 设置浏览量增加时间判断,同一篇文章两次浏览超过五分钟才重新统计阅览量
        u = self.request.user
        ses = self.request.session
        the_key = 'is_read_{}'.format(obj.id)
        is_read_time = ses.get(the_key)
        if not is_read_time:
            obj.update_views()
            ses[the_key] = time.time()
        else:
            now_time = time.time()
            t = now_time - is_read_time
            if t > 60 * 5:
                obj.update_views()
                ses[the_key] = time.time()
        # 获取文章更新的时间，判断是否从缓存中取文章的markdown,可以避免每次都转换
        ud = obj.update_date.strftime("%Y%m%d%H%M%S")
        md_key = '{}_md_{}'.format(obj.id, ud)
        cache_md = cache.get(md_key)
        if cache_md:
            md = cache_md
        else:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
            ])
            obj.body = md.convert(obj.body)
            obj.toc = md.toc
            cache.set(md_key, (obj.body, obj.toc), 60 * 60 * 12)
        return obj
