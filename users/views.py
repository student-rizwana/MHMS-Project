from django.shortcuts import render
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from .forms import UserRegisterForm, LoginForm, UserProfileForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from maids.models import Maid
from bookings.models import Booking

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

@method_decorator(login_required, name='dispatch')
class ProfileView(DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'
    
    def get_object(self):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        return context

@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('users:profile')
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class RoleBasedLoginView(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return '/admin/'
        elif hasattr(user, 'maid_profile') and user.maid_profile:
            return reverse_lazy('maids:maid_dashboard')
        else:
            return reverse_lazy('users:user_dashboard')

@method_decorator(login_required, name='dispatch')
class UserDashboardView(TemplateView):
    template_name = 'users/user_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['approved_maids'] = Maid.objects.filter(is_approved=True, availability=True).order_by('-avg_rating')[:6]
        context['my_bookings'] = Booking.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        return context
