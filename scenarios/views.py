from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .forms import ScenarioForm
from .models import (
    Scenario,
)
try:
    from training.models import Module as TrainingModule
except Exception:
    TrainingModule = None  # safe fallback


def suggest_modules_for_scenario(scenario, limit=3):
    """
    Return up to `limit` module objects relevant to this scenario.
    Safe fallback: returns [] if TrainingModule isn't available.
    """
    if TrainingModule is None:
        return []
    qs = TrainingModule.objects.all()
    stype = getattr(scenario, "scenario_type", None) or \
        getattr(scenario, "type", None)
    if stype:
        hits = qs.filter(
            title__icontains=stype
        )[:limit]
        if hits:
            return list(hits)
    return list(qs.order_by("-id")[:limit])


class ScenarioListView(LoginRequiredMixin, ListView):
    model = Scenario
    template_name = "scenarios/list.html"
    context_object_name = "scenarios"

    def get_queryset(self):
        return (
            Scenario.objects
            .filter(created_by=self.request.user)
            .order_by("-updated_at")
        )


class ScenarioDetailView(LoginRequiredMixin, DetailView):
    model = Scenario
    template_name = "scenarios/detail.html"
    context_object_name = "scenario"

    def get_queryset(self):
        # only allow viewing user-owned scenarios
        return Scenario.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        scenario = ctx["scenario"]
        # This will be [] if TrainingModule isn't importable;
        # templates handle it with {% if suggested_modules %}
        ctx["suggested_modules"] = suggest_modules_for_scenario(scenario)
        return ctx


class ScenarioCreateView(LoginRequiredMixin, CreateView):
    model = Scenario
    template_name = "scenarios/form.html"
    form_class = ScenarioForm

    def get_initial(self):
        initial = super().get_initial()
        hint = self.request.GET.get(
            "template"
        )
        if hint:
            # If your form has a scenario_type field, prefill that; otherwise seed the title.
            if (
                "scenario_type" in self.form_class.base_fields
            ):
                initial["scenario_type"] = hint
            else:
                initial["title"] = f"{hint} scenario"
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # pass the user to the form for per-user unique title validation
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ScenarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Scenario
    template_name = "scenarios/form.html"
    form_class = ScenarioForm

    def get_queryset(self):
        # only allow editing user-owned scenarios
        return Scenario.objects.filter(created_by=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ScenarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Scenario
    template_name = "scenarios/confirm_delete.html"
    success_url = reverse_lazy("scenarios:list")

    def get_queryset(self):
        # only allow deleting user-owned scenarios
        return Scenario.objects.filter(created_by=self.request.user)
