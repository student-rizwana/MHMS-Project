from django.urls import path, include
from . import views

app_name = 'maids'

urlpatterns = [
     path('', views.HomeView.as_view(), name='home'),
       path('list/', views.PublicMaidsListView.as_view(), name='public_list'),
         path('<str:name>/', views.MaidDetailView.as_view(), name='detail'),
    
    # path('register/', views.MaidRegisterView.as_view(), name='maid_register'),  # View missing - registration uses UserCreationForm in forms.py, no CBV yet
    path('dashboard/', views.MaidDashboardView.as_view(), name='maid_dashboard'),
    path('profile/', views.MaidProfileView.as_view(), name='maid_profile'),
    path('profile/update/', views.MaidProfileUpdateView.as_view(), name='maid_profile_update'),
    path('bookings/', views.MaidBookingsView.as_view(), name='maid_bookings'),
    path('availability/', views.ToggleAvailabilityView.as_view(), name='toggle_availability'),
    path('review/create/<int:booking_id>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('booking/<int:pk>/accept/', views.accept_booking, name='accept_booking'),
    path('booking/<int:pk>/reject/', views.reject_booking, name='reject_booking'),
]

