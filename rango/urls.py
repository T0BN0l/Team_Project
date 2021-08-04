from django.shortcuts import render
from django.urls import path, reverse
from django.urls.resolvers import URLPattern
from rango import views
from registration.backends.simple.views import RegistrationView

app_name='rango'


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return reverse('rango:register_profile')


urlpatterns=[
    path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('category/<slug:category_name_slug>/',views.show_category, name='show_category'),
    # path('add_category/', views.add_category,name='add_category'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    # path('restricted/', views.restricted, name='restricted'),
    path('register_profile/', views.register_profile, name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
]
