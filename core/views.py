# Create your views here.


def home(request):
    return render(request, 'core/home.html')
# core/views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from scenarios.models import Scenario
from training.models import Module, Entitlement, Lesson


@login_required
def dashboard(request):
    user = request.user

    # Scenario stats
    qs = Scenario.objects.filter(created_by=user)
    total = qs.count()
    by_status_qs = qs.values('status').annotate(n=Count('id'))
    status_counts = {'draft': 0, 'approved': 0, 'archived': 0}
    for row in by_status_qs:
        status_counts[row['status']] = row['n']
    latest = qs.order_by('-updated_at')[:5]

    # Training / entitlements
    entitlements = Entitlement.objects.filter(user=user).select_related('module')
    modules_total = Module.objects.filter(is_active=True).count()
    preview_lessons = Lesson.objects.filter(module__is_active=True, is_preview=True).count()

    context = {
        'total_scenarios': total,
        'status_counts': status_counts,
        'latest_scenarios': latest,
        'entitlements': entitlements,
        'modules_total': modules_total,
        'preview_lessons': preview_lessons,
    }
    return render(request, 'core/dashboard.html', context)
