# Register your models here.
from django.contrib import admin
from .models import Module, Lesson, Entitlement


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ("order", "title", "is_preview")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "price_cents", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("title",)

    inlines = [LessonInline]

@admin.register(Entitlement)
class EntitlementAdmin(admin.ModelAdmin):
    list_display = ("user", "module", "purchased_at")
    search_fields = ("user__username", "module__title")
    autocomplete_fields = ("user", "module")
