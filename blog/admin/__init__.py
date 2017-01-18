from django.contrib import admin

from blog.admin.post_admin import PostAdmin
from blog.models import Post

admin.site.register(Post, PostAdmin)
