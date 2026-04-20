from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'about', 'used_for', 'image', 'category', 'is_edible']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Plant name', 'minlength': '2', 'required': True}),
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About plant', 'rows': 4, 'required': True}),
            'used_for': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Used for', 'rows': 4, 'required': True}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'is_edible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise forms.ValidationError("Plant name must be at least 2 characters.")
        return name

    def clean_about(self):
        about = self.cleaned_data['about'].strip()
        if len(about) < 10:
            raise forms.ValidationError("About must be at least 10 characters.")
        return about

    def clean_used_for(self):
        used_for = self.cleaned_data['used_for'].strip()
        if len(used_for) < 5:
            raise forms.ValidationError("Used for must be at least 5 characters.")
        return used_for