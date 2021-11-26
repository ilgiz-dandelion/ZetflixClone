
from django.contrib import admin

from main.models import *


class ImageInLine(admin.TabularInline):
    model = Image
    max_num = 6
    min_num = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, ]


admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Likes)
admin.site.register(Reply)
admin.site.register(Rating)

