# training/admin.py
from django.contrib import admin
from django.db import models as dj_models
from django.forms import Textarea

from .models import Module, Lesson, Entitlement


class LessonInline(admin.StackedInline):  # Stacked = better for long text
    model = Lesson
    extra = 0
    fields = ("order", "title", "is_preview", "content")
    formfield_overrides = {
        dj_models.TextField: {
            "widget": Textarea(
                attrs={
                    "rows": 12,
                    "cols": 100
                }
            )
        }
    }


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "price_cents", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title",)
    inlines = [LessonInline]


@admin.register(Lesson)  # edit lessons on their own page too
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "order", "is_preview")
    list_filter = (
        "module",
        "is_preview",
    )
    search_fields = ("title", "module__title")
    ordering = ("module", "order")
    formfield_overrides = {
        dj_models.TextField: {
            "widget": Textarea(attrs={"rows": 18, "cols": 100})
        }
    }


@admin.register(Entitlement)
class EntitlementAdmin(admin.ModelAdmin):
    list_display = ("user", "module", "purchased_at")
    search_fields = ("user__username", "module__title")
    autocomplete_fields = ("user", "module")
