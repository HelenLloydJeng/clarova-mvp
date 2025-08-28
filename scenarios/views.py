from django.shortcuts import render

# Create your views here.
# scenarios/views.py
from django.http import HttpResponse
from django.views import View

class ScenarioListView(View):
    def get(self, request):
        return HttpResponse("Scenarios list (WIP)")

class ScenarioDetailView(View):
    def get(self, request, pk):
        return HttpResponse(f"Scenario detail {pk} (WIP)")

class ScenarioCreateView(View):
    def get(self, request):
        return HttpResponse("Scenario create (WIP)")

class ScenarioUpdateView(View):
    def get(self, request, pk):
        return HttpResponse(f"Scenario edit {pk} (WIP)")

class ScenarioDeleteView(View):
    def get(self, request, pk):
        return HttpResponse(f"Scenario delete {pk} (WIP)")

