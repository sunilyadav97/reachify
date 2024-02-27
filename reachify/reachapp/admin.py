from django.contrib import admin
from reachify.reachapp.models import Platform, SocialProfile, Referral, PlatformEngagementType


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(PlatformEngagementType)
class PlatformEngagementTypeAdmin(admin.ModelAdmin):
    list_display = ['platform', 'engagement_type', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(SocialProfile)
class SocialProfileAdmin(admin.ModelAdmin):
    list_display = ['member', 'platform', 'username', 'old_username', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['member', 'code', 'is_completed', 'created']
    readonly_fields = ['created']
