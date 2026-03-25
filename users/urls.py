from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('login/', views.RoleBasedLoginView.as_view(), name='login'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

