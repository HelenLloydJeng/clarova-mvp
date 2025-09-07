# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class ModuleListView(LoginRequiredMixin, TemplateView):
    template_name = "training/list.html"

