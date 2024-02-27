from django import forms

from reachify.reachapp.models import Promotion, PlatformEngagementType
from reachify.users.models import Member


class PromotionForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_social_profile = self.initial.get('social_profile')
        if initial_social_profile:
            self.fields['social_profile'] = forms.CharField(
                initial=initial_social_profile, disabled=True,
                label="Your Instagram username"
            )
        self.fields['engagement_type'].empty_label = 'Select Promotion Type'
        self.fields['engagement_type'].queryset = PlatformEngagementType.objects.filter(is_active=True)

    class Meta:
        model = Promotion
        fields = [
            'social_profile',
            'engagement_type',
            'target_followers_count',
        ]
        labels = {
            'social_profile': 'Your Instagram username',
            'engagement_type': 'Select Promotion Type',
            'target_followers_count': 'Number of Followers',
        }
