
from django.contrib import admin

from reviews.models import Review


class ReviewAdmin(admin.ModelAdmin):

    list_filter = ['is_active']

    list_display = ['name', 'date_created', 'user', 'rating', 'is_active']

    list_editable = ['is_active']

    search_fields = ['id', 'name', 'text']


admin.site.register(Review, ReviewAdmin)
