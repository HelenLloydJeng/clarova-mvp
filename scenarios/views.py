from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ScenarioForm
from .models import Scenario


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
        return Scenario.objects.filter(created_by=self.request.user)


class ScenarioCreateView(LoginRequiredMixin, CreateView):
    model = Scenario
    template_name = "scenarios/form.html"
    form_class = ScenarioForm

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
