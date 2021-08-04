from django.shortcuts import render
from django.urls import path
from django.urls.resolvers import URLPattern
from rango import views

app_name='rango'


urlpatterns=[
    path('',views.index, name='index'),
    path('about/',views.about, name='about'),
    # path(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category, name='show_category'),
    # # r 表示字符串为非转义的原始字符串，让编译器忽略反斜杠，也就是忽略转义字符。
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
    path('add_category/',views.add_category,name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('search/', views.search, name='search'),
    # path('logout/', views.user_logout, name='logout'),
]