from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'time_update', 'get_html_image', 'author')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('time_create',)
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'cat', 'content', 'image', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_image')
    save_on_top = True

    def get_html_image(self, object):
        if object.image:
             return mark_safe(f"<img src='{object.image.url}' width=60>")

    get_html_image.short_description = "Миниатюра"
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Course, CourseAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Админ-панель сайта о финансах'
admin.site.site_header = 'Админ-панель сайта о финансовой грамотности'
