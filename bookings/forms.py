from django import forms
from crispy_forms.helper import FormHelper
from .models import Booking
from maids.models import Maid
from django.contrib.auth.models import User

class BookingForm(forms.ModelForm):
    booking_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label='Select Date and Time'
    )
    
    service_type = forms.CharField(
        max_length=100,
        required=False,
        label='Service Type (Optional)'
    )
    
    class Meta:
        model = Booking
        fields = ['booking_date', 'service_type']
    
    def __init__(self, *args, **kwargs):
        self.maid = kwargs.pop('maid', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-needs-validation'
        self.helper.form_method = 'post'
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        booking.user = self.user
        booking.maid = self.maid
        if commit:
            booking.save()
        return booking

