from django.contrib import admin
from rango.models import Category, Page, UserProfile, UserView, UserLike


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class UserLikesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'check': ('category', )}


class UserViewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'check': ('page', )}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(UserView, UserViewsAdmin)
admin.site.register(UserLike, UserLikesAdmin)
