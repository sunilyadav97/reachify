import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import requests
from bs4 import BeautifulSoup
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.views.generic import FormView, TemplateView

from reachify.reachapp.api import is_valid_instagram, get_instagram_account_data
from reachify.reachapp.forms import PromotionForm
from reachify.reachapp.models import SocialProfile, PlatformEngagementType, Promotion
from reachify.reachapp.utils import get_instagram_platform
from reachify.users.models import Member
from django.contrib import messages


class HomeView(TemplateView):
    template_name = 'pages/home.html'
    success_url = reverse_lazy("reachapp:dashboard")

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        if username:
            member_exists = Member.objects.filter(username=username).exists()
            if member_exists:
                # Member already exists, redirect to dashboard
                self.request.session['member_username'] = username
                return redirect('reachapp:dashboard')
            else:
                # Member does not exist, verify if it's a valid Instagram account
                is_valid = is_valid_instagram(username)
                if is_valid:
                    insta_object = get_instagram_platform()
                    if insta_object:
                        member = Member.objects.create(username=username)
                        SocialProfile.objects.create(member=member, username=username, platform=insta_object)
                        self.request.session['member_username'] = member.username
                        messages.success(self.request, 'Success!')
                        return redirect('reachapp:dashboard')
                    else:
                        messages.warning(self.request, "please try after some time due to technical issue!")
                        return redirect("reachapp:home")

                else:
                    messages.error(self.request, "Please enter a valid Instagram username.")

        return render(request, self.template_name, {'username': username})


class DashboardView(TemplateView):
    template_name = 'reachapp/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        member_username = self.request.session.get('member_username')
        if member_username:
            self.member = Member.objects.get(username=member_username)
            self.social_profile = SocialProfile.objects.get(member=self.member, is_active=True)
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.info(self.request, 'Please add your Instagram!')
            return redirect("reachapp:home")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['member'] = self.member
        account_data = get_instagram_account_data(self.member.username)
        ctx['account_data'] = account_data
        return ctx


class AddPromotionView(FormView):
    form_class = PromotionForm
    template_name = "reachapp/promotion_form.html"

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

    def form_valid(self, form):
        engagement_type = form.cleaned_data.get("engagement_type")
        target_followers_count = form.cleaned_data.get("target_followers_count")
        credits_required = engagement_type.credits * target_followers_count
        self.credits_required = credits_required
        if credits_required <= self.member.get_available_credits:
            instance = Promotion.objects.create(
                social_profile=self.social_profile,
                engagement_type=engagement_type,
                credits_required=credits_required,
                target_followers_count=target_followers_count,
                start_date=datetime.now()
            )
            if instance:
                self.member.used_credit += credits_required
                self.member.save()
            messages.success(self.request, 'Your promotion has been set successfully!')
            return redirect("reachapp:dashboard")
        else:
            messages.warning(self.request, "You don't have sufficient credits! Please earn more credits.")
            form.add_error('target_followers_count', "You don't have sufficient credits! Please earn more credits.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['member'] = self.member
        ctx['credits_required'] = self.credits_required
        return ctx


def platform_engagement_credits_view(request, id):
    """ API for getting platform engagement type credits"""
    engagement_instance = PlatformEngagementType.objects.get(id=id)
    data = {}
    if engagement_instance:
        data['credits'] = engagement_instance.credits
    json_data = json.dumps(data)
    return JsonResponse(json_data, safe=False)
