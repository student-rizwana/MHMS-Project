from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from .forms import PaymentForm
from .models import Payment
from bookings.models import Booking


class PaymentProcessView(LoginRequiredMixin, FormView):
    form_class = PaymentForm
    template_name = 'payments/payment.html'
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.booking = get_object_or_404(Booking, id=kwargs['booking_id'], user=request.user)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = Payment(booking=self.booking)
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.booking
        context['maid'] = self.booking.maid
        context['total_amount'] = self.booking.amount or 500.00  # Use booking amount or default
        if hasattr(self.booking, 'payment'):
            context['existing_payment'] = self.booking.payment
        return context
    
    def form_valid(self, form):
        payment = form.save(commit=False)
        payment.booking = self.booking
        
        # Check for existing payment
        existing = Payment.objects.filter(booking=self.booking).first()
        if existing and existing.status == 'completed':
            messages.warning(self.request, 'Payment already completed for this booking.')
            return redirect(reverse('payments:confirm', kwargs={'booking_id': self.booking.id}))
        
        payment.amount = form.cleaned_data['amount']
        payment.status = 'completed'
        payment.transaction_id = f'TXN{self.booking.id}{timezone.now().timestamp()}'
        payment.paid_at = timezone.now()
        payment.save()
        
        self.booking.status = 'confirmed'
        self.booking.save()
        
        messages.success(self.request, 'Payment successful! Booking confirmed.')
        return redirect(reverse('payments:confirm', kwargs={'booking_id': self.booking.id}))
    
    def get_success_url(self):
        return reverse('payments:confirm', kwargs={'booking_id': self.booking.id})
    
    def form_invalid(self, form):
        messages.error(self.request, 'Payment form invalid. Please check amount.')
        return super().form_invalid(form)


class PaymentConfirmView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/payment_confirm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_id = kwargs['booking_id']
        booking = get_object_or_404(Booking, id=booking_id, user=self.request.user)
        context['booking'] = booking
        context['payment'] = booking.payment
        return context


class PaymentHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/history.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payments = Payment.objects.filter(booking__user=self.request.user).order_by('-paid_at')
        context['payments'] = payments
        return context

