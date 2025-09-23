from django.contrib import admin
from .models import Organisation, UserProfile


@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sector', 'created_at')
    search_fields = ('name', 'sector')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organisation', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'organisation__name')
