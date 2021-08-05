from django.shortcuts import render
from django.urls import path, reverse
from django.urls.resolvers import URLPattern
from registration.backends.simple.views import RegistrationView

from rango import views

app_name = 'rango'


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('rango:register_profile')


urlpatterns = [
    path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    path('about/', views.AboutView.as_view(), name='about'),
    # path(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category, name='show_category'),
    # # r 表示字符串为非转义的原始字符串，让编译器忽略反斜杠，也就是忽略转义字符。
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    # =======================================================
    # path('add_category/', views.add_category, name='add_category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    # ================================================================
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('restricted/', views.restricted, name='restricted'),
    path('search/', views.search, name='search'),
    # path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),
    path('suggest/', views.suggest_category, name='suggest'),
    # path('logout/', views.user_logout, name='logout'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    # ====================================================
    # path('profile/', views.profile, name='profile'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),

]
