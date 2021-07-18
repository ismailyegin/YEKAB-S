from django.contrib import admin

from ekabis.models.ActiveGroup import ActiveGroup
from ekabis.models.PermissionGroup import PermissionGroup
from ekabis.models.Menu import Menu
from ekabis.models.Country import Country
from ekabis.models.City import City
from ekabis.models.Settings import Settings
from ekabis.models.CompanyFiles import CompanyFiles
from ekabis.models.CompanyFileNames import CompanyFileNames
from ekabis.models.CompanyUser import CompanyUser
from ekabis.models.YekaBusinessBlog import YekaBusinessBlog
from ekabis.models.CalendarName import CalendarName
from ekabis.models.Calendar import Calendar

admin.site.site_header = 'Kobiltek Bilisim Kullanici Yönetim Paneli '  # default: "Django Administration"
admin.site.index_title = 'Sistem Yönetimi'  # default: "Site administration"
admin.site.site_title = 'Admin'  # default: "Django site admin"

admin.site.register(CompanyFiles)
admin.site.register(CompanyFileNames)
admin.site.register(ActiveGroup)
admin.site.register(PermissionGroup)
admin.site.register(Menu)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Settings)
admin.site.register(Calendar)
admin.site.register(CalendarName)
admin.site.register(YekaBusinessBlog)
