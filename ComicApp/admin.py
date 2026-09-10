from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Comment, Comic, ComicPage, CustomUser, Like

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Comic)
admin.site.register(ComicPage)
admin.site.register(Comment)
admin.site.register(Like)
