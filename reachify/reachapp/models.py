from django.db import models
from django_extensions.db.models import TimeStampedModel

from reachify.users.models import Member


class Platform(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    link = models.URLField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PlatformEngagementType(TimeStampedModel):
    platform = models.ForeignKey("Platform", on_delete=models.CASCADE)
    engagement_type = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.platform.name} {self.engagement_type}"


class SocialProfile(TimeStampedModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True)
    old_username = models.CharField(max_length=150, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.member.username} - {self.platform.name}"


class Promotion(TimeStampedModel):
    social_profile = models.ForeignKey("SocialProfile", on_delete=models.CASCADE)
    engagement_type = models.ForeignKey("PlatformEngagementType", null=True, on_delete=models.SET_NULL)
    target_followers_count = models.PositiveIntegerField()  # Number of followers member wants
    achieved_follower_count = models.PositiveIntegerField(default=0)  # Number of followers member has achieved
    credits_required = models.PositiveIntegerField(default=0)  # Credits required for this promotion
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.social_profile.member.username} - {self.target_followers_count}"


class Referral(TimeStampedModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    code = models.CharField(max_length=80, unique=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.username} - {self.code}"
