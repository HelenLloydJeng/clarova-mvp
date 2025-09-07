from django.urls import path
from . import views

app_name = "training"
urlpatterns = [
    path("", views.ModuleListView.as_view(), name="list"),
    path("<int:pk>/", views.ModuleDetailView.as_view(), name="detail"),
]
