from django.contrib import messages
from django.core.exceptions import ValidationError, FieldError
from django.db import models
from django.db.models.functions import datetime
from django_extensions.db.models import TimeStampedModel
from django_lifecycle import hook, BEFORE_UPDATE, BEFORE_SAVE, AFTER_UPDATE, AFTER_DELETE
from django_lifecycle.conditions import WhenFieldHasChanged
from django_lifecycle.mixins import LifecycleModelMixin
from django.utils.datetime_safe import datetime

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
    credits = models.PositiveIntegerField(default=2)
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


class Promotion(LifecycleModelMixin, TimeStampedModel):
    social_profile = models.ForeignKey("SocialProfile", on_delete=models.CASCADE)
    engagement_type = models.ForeignKey("PlatformEngagementType", null=True, on_delete=models.SET_NULL)
    link = models.URLField(null=True, blank=True, help_text="link of post")
    target_followers_count = models.PositiveIntegerField()  # Number of followers member wants
    achieved_follower_count = models.PositiveIntegerField(default=0)  # Number of followers member has achieved
    credits_required = models.PositiveIntegerField(default=0)  # Credits required for this promotion
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.social_profile.member.username} - {self.target_followers_count}"

    @hook(BEFORE_UPDATE, condition=WhenFieldHasChanged("achieved_follower_count", has_changed=True))
    def track_achieved_follower_count(self):
        """If achieved_follower_count is equal to target_followers_count then complete the promotion."""
        if self.achieved_follower_count == self.target_followers_count:
            self.is_completed = True
            self.end_date = datetime.now()

        if self.achieved_follower_count > self.target_followers_count:
            raise FieldError('Achieved follower count can not greater then target followers count')

    @hook(AFTER_DELETE)
    def update_social_profile_credits(self):
        member = self.social_profile.member
        if not self.is_completed and self.is_active:
            if self.achieved_follower_count < self.target_followers_count:
                due_followers_count = self.target_followers_count - self.achieved_follower_count
                refund_credit = due_followers_count*self.engagement_type.credits
                member.used_credit -= refund_credit
                member.save()


class PromotionInteraction(TimeStampedModel):
    promoter = models.ForeignKey("SocialProfile", related_name='interactions_given', on_delete=models.CASCADE)
    promotion = models.ForeignKey("Promotion", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('promoter', 'promotion')


class Referral(TimeStampedModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    code = models.CharField(max_length=80, unique=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.member.username} - {self.code}"
