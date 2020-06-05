import xadmin
from .models import (
        Timeline,
        FriendLink,
        Activate, 
    )


@xadmin.sites.register(Timeline)
class TimelineAdmin(object):
    list_display = ('title', 'side', 'update_date', 'icon', 'icon_color',)
    fieldsets = (
        ('图标信息', {'fields': (('icon', 'icon_color'),)}),
        ('时间位置', {'fields': (('side', 'update_date', 'star_num'),)}),
        ('主要内容', {'fields': ('title', 'content')}),
    )
    date_hierarchy = 'update_date'
    list_filter = ('star_num', 'update_date')


@xadmin.sites.register(FriendLink)
class FriendLinkAdmin(object):
    list_display = ('name', 'description', 'link', 'create_date', 'is_active', 'is_show')
    date_hierarchy = 'create_date'
    list_filter = ('is_active', 'is_show')


@xadmin.sites.register(Activate)
class ActivateAdmin(object):
    list_display = ('content', 'is_active', 'add_date')
