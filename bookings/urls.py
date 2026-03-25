from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<str:maid_name>/', views.BookingCreateView.as_view(), name='book_maid'),
    path('confirm/<int:pk>/', views.BookingConfirmView.as_view(), name='booking_confirm'),
]

