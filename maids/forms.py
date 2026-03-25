from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Maid, Review
from bookings.models import Booking
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML
from crispy_forms.bootstrap import InlineRadios

class MaidRegisterForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)
    skills = forms.CharField(widget=forms.Textarea, help_text="Comma-separated: Cleaning, Cooking, etc.")
    experience = forms.IntegerField(min_value=0, help_text="Years of experience")
    location = forms.CharField(max_length=100, required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'phone', 'skills', 'experience', 'location', 'photo')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            maid = Maid.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                phone=self.cleaned_data['phone'],
                skills=self.cleaned_data['skills'],
                experience=self.cleaned_data['experience'],
                location=self.cleaned_data['location'],
                photo=self.cleaned_data.get('photo')
            )
        return user

class MaidUpdateForm(forms.ModelForm):
    class Meta:
        model = Maid
        fields = ['photo', 'skills', 'experience', 'location', 'phone']
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
            'phone': forms.TextInput(attrs={'placeholder': '+91XXXXXXXXXX'}),
        }

class AvailabilityToggleForm(forms.Form):
    availability = forms.BooleanField(required=False)

class BookingActionForm(forms.Form):
    action = forms.ChoiceField(choices=[('accept', 'Accept'), ('reject', 'Reject')])

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'★{'★'*(i-1)} ({i}/5)') for i in range(1,6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'needs-validation'
        self.helper.layout = Layout(
            HTML('<h5>Add Your Review</h5>'),
            InlineRadios('rating'),
            'comment',
            Submit('submit-review', 'Submit Review', css_class='btn btn-primary mt-3')
        )
        self.fields['rating'].label = False
        self.fields['comment'].label_class = 'form-label fw-bold'

