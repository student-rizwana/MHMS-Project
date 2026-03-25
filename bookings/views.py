from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from django.http import Http404
from .forms import BookingForm
from maids.models import Maid
from .models import Booking
from django.contrib.auth.models import User

class BookingCreateView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.maid = get_object_or_404(Maid, name=kwargs['maid_name'])
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['maid'] = self.maid
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if not self.maid.availability:
            messages.error(self.request, 'Maid is currently unavailable.')
            return redirect('maids:maid_detail', self.maid.name)
        messages.success(self.request, 'Booking request created successfully! Awaiting maid confirmation.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('bookings:booking_confirm', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maid'] = self.maid
        return context


class BookingConfirmView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_confirm.html'
    context_object_name = 'booking'
    
    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise Http404
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['maid'] = self.object.maid
        return context

