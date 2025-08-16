from django import forms
from .models import Organisation

class OrganisationCreateForm(forms.ModelForm):
    class Meta:
        model = Organisation
        fields = ['name', 'sector']

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 3:
            raise forms.ValidationError("Organisation name must be at least 3 characters.")
        return name
