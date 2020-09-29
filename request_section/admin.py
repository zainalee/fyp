from django.contrib import admin

from .models import PostRequest, Comment


admin.site.register(PostRequest)
admin.site.register(Comment)
