from django.urls import path
from . import views

app_name = "training"
urlpatterns = [
    path("", views.ModuleListView.as_view(), name="list"),
    path("<int:pk>/", views.ModuleDetailView.as_view(), name="detail"),
    path("<int:pk>/checkout/", views.checkout_create, name="checkout"),
    path("checkout/success/", views.checkout_success, name="success"),
    path("checkout/cancel/", views.checkout_cancel, name="cancel"),

]
