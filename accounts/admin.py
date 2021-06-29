from django.contrib import admin

from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.models.Menu import Menu

admin.site.site_header = 'Kobiltek Bilisim Kullanici Yönetim Paneli '  # default: "Django Administration"
admin.site.index_title = 'Sistem Yönetimi'  # default: "Site administration"
admin.site.site_title = 'Admin'  # default: "Django site admin"


admin.site.register(ActiveGroup)
admin.site.register(PermissionGroup)
admin.site.register(Menu)
