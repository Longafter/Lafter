from django.urls import path

from .views import (
        IndexView, 
        CategoryView, 
        TagView, 
        ArchiveView, 
        ArticleDetailView, 
    )

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('tag/<slug:slug>/', TagView.as_view(), name='tag'),
    path('archive/', ArchiveView.as_view(), name='archive'),
]
