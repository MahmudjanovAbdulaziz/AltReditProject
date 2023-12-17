from django.contrib import admin
from django.utils.text import slugify
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.html import format_html

from .models import *


class CreateNewRaditAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'text', 'likes')
    prepopulated_fields = {"post_slug": ("title", )}
    

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)



class LikeInline(GenericTabularInline):
    model = Like
    extra = 0

class ReviewsAboutSiteAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'like_count')
    inlines = [LikeInline]

    def like_count(self, obj):
        return obj.likes.count()

    like_count.short_description = 'Likes Count'

class CommentDetailAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'text', 'like_count')
    inlines = [LikeInline]

    def like_count(self, obj):
        return obj.likes.count()

    like_count.short_description = 'Likes Count'

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'avatar_display')
    readonly_fields = ('avatar_display',)

    def avatar_display(self, obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.avatar.url))

    avatar_display.short_description = 'Avatar Preview'

admin.site.register(ReviewsAboutSite, ReviewsAboutSiteAdmin)
admin.site.register(CommentDetail, CommentDetailAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CreateNewRadit, CreateNewRaditAdmin)
admin.site.register(Like)


