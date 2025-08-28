from django.conf import settings
from django.db import models
from django.urls import reverse

SEVERITY = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("high", "High"),
    ("critical", "Critical"),
]

STATUS = [
    ("draft", "Draft"),
    ("approved", "Approved"),
    ("archived", "Archived"),
]


class Scenario(models.Model):
    title = models.CharField(max_length=120)
    summary = models.TextField(blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY, default="low")
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    # keep org optional for MVP so it doesn't block you
    organisation = models.CharField(max_length=120, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scenarios",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["title", "created_by"],
                name="uniq_scenario_title_per_user",
            )
        ]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("scenarios:detail", args=[self.pk])


class ScenarioReview(models.Model):
    scenario = models.ForeignKey(
        Scenario, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey( 
        
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="scenario_reviews",
    )
    decision = models.CharField(
        max_length=10,
        choices=[("approve", "Approve"), ("reject", "Reject")],
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.reviewer} → {self.scenario} ({self.decision})"
