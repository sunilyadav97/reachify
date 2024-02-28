from django import forms

from reachify.reachapp.models import Promotion, PlatformEngagementType


class PromotionForm(forms.ModelForm):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['engagement_type'].empty_label = 'Select Promotion Type'
        self.fields['engagement_type'].queryset = PlatformEngagementType.objects.filter(is_active=True)

    class Meta:
        model = Promotion
        fields = [
            'engagement_type',
            'target_followers_count',
        ]
        labels = {
            'engagement_type': 'Select Promotion Type',
            'target_followers_count': 'Number of Followers',
        }
