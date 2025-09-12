# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from .models import Module, Lesson, Entitlement
# Stripe + helpers
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseNotAllowed
from django.urls import reverse



class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = "training/list.html"
    context_object_name = "modules"

    def get_queryset(self):
        return Module.objects.order_by("title")
     
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

    def get_queryset(self):
        return Module.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        module = self.object
        has_access = Entitlement.objects.filter(
            user=self.request.user, module=module
        ).exists()
        lessons = (
            module.lessons.all()
            if has_access
            else module.lessons.filter(is_preview=True)
        )
        ctx["has_access"] = has_access
        ctx["lessons"] = lessons
        return ctx
# --- Stripe Checkout (MVP) ---
@login_required
def checkout_create(request, pk):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    module = get_object_or_404(Module, pk=pk)

    # If already owned, bounce back
    if Entitlement.objects.filter(user=request.user, module=module).exists():
        return redirect(module.get_absolute_url())

    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Absolute URLs for redirect
    success_url = request.build_absolute_uri(
        reverse("training:success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri(module.get_absolute_url())

    session = stripe.checkout.Session.create(
        mode="payment",
        client_reference_id=str(module.pk),
        customer_email=(request.user.email or None),
        line_items=[{
            "price_data": {
                "currency": "gbp",
                "product_data": {"name": module.title},
                "unit_amount": module.price_cents,
            },
            "quantity": 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return redirect(session.url, permanent=False)


@login_required
def checkout_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return render(request, "training/checkout_success.html", {"ok": False, "error": "Missing session id."})

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        return render(request, "training/checkout_success.html", {"ok": False, "error": str(e)})

    if session.get("payment_status") == "paid":
        module_id = int(session.get("client_reference_id") or 0)
        module = Module.objects.filter(pk=module_id).first()
        if module:
            Entitlement.objects.get_or_create(user=request.user, module=module)
        return render(request, "training/checkout_success.html", {"ok": True, "module": module})

    return render(
        request,
        "training/checkout_success.html",
        {"ok": False, "error": f"Payment status: {session.get('payment_status')}"}
    )


@login_required
def checkout_cancel(request):
    return render(request, "training/checkout_cancel.html")
