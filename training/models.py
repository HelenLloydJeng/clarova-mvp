# Create your models here.
from django.conf import settings
from django.db import models
from django.urls import reverse


class Module(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price_cents = models.PositiveIntegerField(default=0)  # Stripe-friendly
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("training:detail", args=[self.pk])


class Lesson(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lessons"
    )
    title = models.CharField(max_length=160)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "id"]
        constraints = [
            models.UniqueConstraint(
                fields=["module", "order"], name="uniq_lesson_order_per_module"
            )
        ]

    def __str__(self) -> str:
        return f"{self.module.title} · {self.title}"


class Entitlement(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="entitlements",
    )
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="entitlements"
    )
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-purchased_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "module"], name="uniq_entitlement_user_module"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} → {self.module}"

