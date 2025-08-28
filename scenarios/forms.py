# scenarios/forms.py
from django import forms
from .models import Scenario

class ScenarioForm(forms.ModelForm):
    """ModelForm with per-user unique title validation."""
    class Meta:
        model = Scenario
        fields = ["title", "summary", "severity", "status", "organisation"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Data breach at HQ"}),
            "summary": forms.Textarea(attrs={"rows": 4, "placeholder": "One-paragraph overview"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            return title
        if self.user:
            qs = Scenario.objects.filter(created_by=self.user, title__iexact=title)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("You already have a Scenario with this title.")
        return title
