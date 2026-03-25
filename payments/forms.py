from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '1'}),
        }
    
    def __init__(self, *args, **kwargs):
        total_amount = kwargs.pop('total_amount', 500.00)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('amount', placeholder=f'Amount (₹{total_amount})')
        )
        self.fields['amount'].initial = total_amount
        self.fields['amount'].label = False
    
    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than 0.')
        return amount

