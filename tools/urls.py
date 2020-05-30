from django.urls import path

from .views import (
        TimelineView, 
        CarouselView, 
        FriendLinkView, 
    )

app_name = 'tools'

urlpatterns = [
    path('timeline/', TimelineView.as_view(), name='timeline'),
    path('friendlink/', FriendLinkView.as_view(), name='friendlink'),
]
