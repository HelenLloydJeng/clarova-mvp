# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OrganisationCreateForm
from .models import UserProfile

@login_required
def create_organisation(request):
    if request.method == 'POST':
        form = OrganisationCreateForm(request.POST)
        if form.is_valid():
            org = form.save()
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.organisation = org
            # Promote first creator to admin if still default role
            if profile.role == UserProfile.ROLE_EDITOR:
                profile.role = UserProfile.ROLE_ADMIN
            profile.save()
            return redirect('core:home')
    else:
        form = OrganisationCreateForm()
    return render(request, 'accounts/org_create.html', {'form': form})

