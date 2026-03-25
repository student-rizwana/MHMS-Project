from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('process/<int:booking_id>/', views.PaymentProcessView.as_view(), name='process'),
    path('confirm/<int:booking_id>/', views.PaymentConfirmView.as_view(), name='confirm'),
]

