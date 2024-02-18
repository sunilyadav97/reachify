from django.core.exceptions import ValidationError

from reachify.users.models import Member


def validate_unique_username(value):
    if Member.objects.filter(username=value).exists():
        raise ValidationError("Username already exists.")
