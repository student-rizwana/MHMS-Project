from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'maid', 'booking_date', 'status']
    list_filter = ['status']
    search_fields = ['user__username', 'maid__name']

