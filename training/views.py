# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from .models import Module, Lesson, Entitlement

class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = "training/list.html"
    context_object_name = "modules"

    def get_queryset(self):
        return Module.objects.filter(is_active=True).order_by("title")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            owned = set(
                Entitlement.objects.filter(user=self.request.user)
                .values_list("module_id", flat=True)
            )
        else:
            owned = set()
        ctx["owned_ids"] = owned
        return ctx

class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = "training/detail.html"
    context_object_name = "module"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = self.object
        has_access = Entitlement.objects.filter(
            user=self.request.user, module=module
        ).exists()
        lessons = module.lessons.all() if has_access else module.lessons.filter(is_preview=True)
        ctx["has_access"] = has_access
        ctx["lessons"] = lessons
        return ctx
