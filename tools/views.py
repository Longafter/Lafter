from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from .models import Timeline, FriendLink


class TimelineView(ListView):
    model = Timeline
    template_name = 'tools/timeline.html'
    context_object_name = 'timeline_list'


class FriendLinkView(ListView):
    model = FriendLink
    template_name = 'tools/friendlink.html'
    context_object_name = 'friendlink_list'
