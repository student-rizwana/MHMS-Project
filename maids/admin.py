from django.contrib import admin
from .models import Maid, Review

@admin.register(Maid)
class MaidAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'availability', 'avg_rating', 'is_approved']
    list_filter = ['availability', 'is_approved']
    search_fields = ['name', 'location']
    readonly_fields = ['avg_rating']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['maid', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['maid__name', 'user__username', 'comment']
    date_hierarchy = 'created_at'

