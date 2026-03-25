from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Avg
from django.urls import reverse_lazy, reverse
from .models import Maid, Review
from .forms import MaidRegisterForm, MaidUpdateForm, AvailabilityToggleForm, BookingActionForm, ReviewForm
from bookings.models import Booking
from django.db.models import Avg
from django.http import JsonResponse

class HomeView(ListView):
    model = Maid
    template_name = 'home.html'
    context_object_name = 'object_list'
    paginate_by = None

    def get_queryset(self):
        return Maid.objects.filter(is_approved=True, availability=True).order_by('-avg_rating')[:4]

class PublicMaidsListView(ListView):
    model = Maid
    template_name = 'maids/public_dashboard.html'
    context_object_name = 'maids'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Maid.objects.filter(availability=True).order_by('-avg_rating')
        skills = self.request.GET.get('skills')
        location = self.request.GET.get('location')
        min_exp = self.request.GET.get('experience')
        if skills:
            queryset = queryset.filter(skills__icontains=skills)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_exp:
            queryset = queryset.filter(experience__gte=int(min_exp))
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET
        return context

class MaidDetailView(DetailView):
    model = Maid
    template_name = 'maids/maid_detail.html'
    context_object_name = 'maid'
    slug_field = 'name'
    slug_url_kwarg = 'name'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.object.reviews.all()
        context['reviews'] = reviews
        context['avg_rating'] = self.object.avg_rating
        
        if self.request.user.is_authenticated:
            from bookings.models import Booking
            context['user_bookings'] = Booking.objects.filter(
                user=self.request.user, 
                maid=self.object, 
                status='confirmed'
            )
        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'maids/review_form.html'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.booking = get_object_or_404(Booking, pk=kwargs['booking_id'], user=request.user)
    
    def get_initial(self):
        self.initial = super().get_initial()
        self.initial['maid'] = self.booking.maid.id
        self.initial['user'] = self.request.user.id
        return self.initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.booking
        context['maid'] = self.booking.maid
        return context
    
    def form_valid(self, form):
        form.instance.maid = self.booking.maid
        form.instance.user = self.request.user
        
        # Prevent duplicate - check by user + maid only since no booking_id field
        existing = Review.objects.filter(user=self.request.user, maid=self.booking.maid).exists()
        if existing:
            messages.error(self.request, 'You already submitted a review for this maid.')
            return redirect('maids:detail', name=self.booking.maid.name)
        
        response = super().form_valid(form)
        messages.success(self.request, 'Thank you for your review!')
        return response
    
    def get_success_url(self):
        return reverse('maids:detail', kwargs={'name': self.booking.maid.name})

# New additions: Maid-specific mixin and views
class MaidMixin(LoginRequiredMixin):
    """Mixin to ensure user has a Maid profile"""
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'maid'):
            messages.error(request, 'You need a maid profile to access this page.')
            return redirect('maids:maid_register')  # or login/register
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maid'] = self.request.user.maid
        return context

class MaidDashboardView(MaidMixin, TemplateView):
    template_name = 'maids/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maid = self.request.user.maid
        context['pending_bookings'] = Booking.objects.filter(maid=maid, status='pending')[:5]
        context['total_bookings'] = Booking.objects.filter(maid=maid).count()
        context['avg_rating'] = maid.avg_rating
        return context

class MaidProfileView(MaidMixin, TemplateView):
    template_name = 'maids/maid_profile.html'

class MaidProfileUpdateView(MaidMixin, UpdateView):
    model = Maid
    form_class = MaidUpdateForm
    template_name = 'maids/maid_profile_update.html'
    
    def get_object(self):
        return self.request.user.maid
    
    def get_success_url(self):
        messages.success(self.request, 'Profile updated successfully!')
        return reverse('maids:maid_profile')

class MaidBookingsView(MaidMixin, ListView):
    model = Booking
    template_name = 'maids/maid_bookings.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(maid=self.request.user.maid).order_by('-created_at')

class ToggleAvailabilityView(MaidMixin, FormView):
    form_class = AvailabilityToggleForm
    template_name = 'maids/toggle_availability.html'
    
    def form_valid(self, form):
        maid = self.request.user.maid
        maid.availability = form.cleaned_data['availability']
        maid.save()
        messages.success(self.request, f'Availability updated to {"Available" if maid.availability else "Unavailable"}!')
        return JsonResponse({'success': True, 'availability': maid.availability})
    
    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors})

def accept_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, maid=request.user.maid)
    if booking.status == 'pending':
        booking.status = 'accepted'
        booking.save()
        messages.success(request, 'Booking accepted!')
    return redirect('maids:maid_bookings')

def reject_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, maid=request.user.maid)
    if booking.status == 'pending':
        booking.status = 'rejected'
        booking.save()
        messages.success(request, 'Booking rejected!')
    return redirect('maids:maid_bookings')
