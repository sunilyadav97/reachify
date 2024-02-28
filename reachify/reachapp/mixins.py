from django.contrib import messages
from django.shortcuts import redirect

from reachify.reachapp.models import SocialProfile
from reachify.users.models import Member


class MemberRequired:

    def dispatch(self, request, *args, **kwargs):
        member_username = self.request.session.get('member_username')
        if member_username:
            self.member = Member.objects.get(username=member_username)
            self.social_profile = SocialProfile.objects.get(member=self.member, is_active=True)
            self.credits_required = 0
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(self.request, 'Please add your Instagram!')
            return redirect("reachapp:home")
