from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name',
                'minlength': '2',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
                'minlength': '2',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message',
                'rows': 6,
                'minlength': '10',
                'required': True
            }),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].strip()
        if len(first_name) < 2:
            raise forms.ValidationError("First name must be at least 2 characters.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name'].strip()
        if len(last_name) < 2:
            raise forms.ValidationError("Last name must be at least 2 characters.")
        return last_name

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < 10:
            raise forms.ValidationError("Message must be at least 10 characters.")
        return message