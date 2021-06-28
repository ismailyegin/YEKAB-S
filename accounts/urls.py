# import patterns as patterns
from django.conf.urls import url
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.login, name='login'),
    path('forgot/', views.forgot, name='view_forgot'),
    path('logout/', views.pagelogout, name='view_logout'),
    path('permission/Add', views.show_urls, name='add_permission'),
]
