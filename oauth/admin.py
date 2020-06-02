import xadmin
from .models import Ouser


# @xadmin.site.register(Ouser)
class OuserAdmin(object):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'date_joined')
    fieldsets = (
        ('基础信息', {'fields': (('username', 'email'), ('link',))}),
        ('重要日期', {'fields': (('last_login', 'date_joined'),)}),
        ('权限信息', {'fields': (('is_active', 'is_staff', 'is_superuser'),
                             'groups', 'user_permissions')}),
    )
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')

xadmin.site.unregister(Ouser)
xadmin.site.register(Ouser, OuserAdmin)
