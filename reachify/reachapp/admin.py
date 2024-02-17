from django.contrib import admin
from .models import Platform, SocialProfile, Referral


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(SocialProfile)
class SocialProfileAdmin(admin.ModelAdmin):
    list_display = ['member', 'platform', 'username', 'old_username', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['member', 'code', 'is_completed', 'created']
    readonly_fields = ['created']
