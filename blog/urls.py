from django.urls import path

from .views import (
        IndexView, 
        ArticleDetailView, 
        CategoryView, 
        TagView, 
        ArchiveView, 
        AboutView, 
    )

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),  # 主页，自然排序
    path('hot/', IndexView.as_view(), {'sort': 'v'}, name='index_hot'),  # 主页，按照浏览量排序
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('category/<slug:slug>/hot/', CategoryView.as_view(), {'sort': 'v'}, name='category_hot'),
    path('tag/<slug:slug>/', TagView.as_view(), name='tag'),
    path('tag/<slug:slug>/hot/', TagView.as_view(), {'sort': 'v'}, name='tag_hot'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('about/', AboutView, name='about'),
]
