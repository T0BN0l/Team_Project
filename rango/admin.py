from django.contrib import admin
from rango.models import Category, Page, UserProfile, UserViews, UserLikes


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class UserViewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'view_page')


class UserLikesAdmin(admin.ModelAdmin):
    list_display = ('user', 'liked_title')


class UserViewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'url')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(UserViews, UserViewsAdmin)
admin.site.register(UserLikes, UserLikesAdmin)
