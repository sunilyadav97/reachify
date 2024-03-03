from django.contrib import admin
from reachify.reachapp.models import Platform, SocialProfile, Referral, PlatformEngagementType, Promotion, \
    PromotionInteraction


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'link', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(PlatformEngagementType)
class PlatformEngagementTypeAdmin(admin.ModelAdmin):
    list_display = ['platform', 'engagement_type', 'credits', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(SocialProfile)
class SocialProfileAdmin(admin.ModelAdmin):
    list_display = ['member', 'platform', 'username', 'old_username', 'is_active', 'created']
    readonly_fields = ['created']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'social_profile',
        'engagement_type',
        'target_followers_count',
        'achieved_follower_count',
        'credits_required',
        'start_date',
        'is_completed',
        'is_active',
        'created',
    ]
    list_filter = ['social_profile', 'engagement_type', 'is_completed', 'is_active']
    readonly_fields = ['created']


@admin.register(PromotionInteraction)
class PromotionInteractionAdmin(admin.ModelAdmin):
    list_display = [
        'promoter',
        'promotion',
        'created',
        'modified'
    ]
    search_fields = ['promoter', 'promotion']
    readonly_fields = ['created']


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ['member', 'code', 'is_completed', 'created']
    readonly_fields = ['created']
