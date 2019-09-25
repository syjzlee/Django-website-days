from django.contrib import admin
from blog.models import Categorys,Tags,Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','auth','created_time','update_time','abstract']


admin.site.register(Categorys)
admin.site.register(Tags)
admin.site.register(Article,ArticleAdmin)