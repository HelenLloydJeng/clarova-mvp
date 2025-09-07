from django.urls import path, include
from . import views

app_name = 'scenarios'

urlpatterns = [
    path('', views.ScenarioListView.as_view(), name='list'),
    path('new/', views.ScenarioCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ScenarioDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ScenarioUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ScenarioDeleteView.as_view(), name='delete'),
    path('training/', include('training.urls')),

]
