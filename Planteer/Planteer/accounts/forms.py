from django import forms
from django.contrib.auth.models import User
import re

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "password"]

  
    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email
  
  
    def clean_username(self):
        username = self.cleaned_data["username"]

        if len(username) < 8:
            raise forms.ValidationError("Username must be at least 8 characters.")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise forms.ValidationError("Only letters, numbers, underscore allowed.")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username


    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")

        if first_name and not first_name.isalpha():
            self.add_error("first_name", "Only letters allowed.")

        if last_name and not last_name.isalpha():
            self.add_error("last_name", "Only letters allowed.")

        return cleaned_data


    def clean_about(self):
        about = self.cleaned_data.get("about")

        if about and len(about) < 5:
            raise forms.ValidationError("About must be at least 5 characters.")

        if about and len(about) > 200:
            raise forms.ValidationError("About must be less than 200 characters.")

        return about


    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if avatar and not avatar.content_type.startswith("image/"):
            raise forms.ValidationError("Avatar must be an image file.")

        return avatar


    def clean_password(self):
        password = self.cleaned_data["password"]

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters.")

        if not any(c.isdigit() for c in password):
            raise forms.ValidationError("Password must contain a number.")

        if not any(c.isalpha() for c in password):
            raise forms.ValidationError("Password must contain a letter.")

        return password

