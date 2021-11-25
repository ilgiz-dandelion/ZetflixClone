from django.contrib import admin

from django.contrib import admin

from main.models import *


class ImageInLine(admin.TabularInline):
    model = Image
    max_num = 6
    min_num = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ]


admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Review)
admin.site.register(Reply)

