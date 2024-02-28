from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_extensions.db.models import TimeStampedModel


class User(AbstractUser):
    """
    Default custom user model for Reachify.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Member(TimeStampedModel):
    username = models.CharField(max_length=150, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    earned_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    purchased_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    used_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    @property
    def get_available_credits(self) -> int:
        total_credits = self.earned_credit + self.purchased_credit
        return int(total_credits - self.used_credit)
