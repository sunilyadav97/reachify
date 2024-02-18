from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from reachify.reachapp.api import is_valid_instagram, get_instagram_account_data
from reachify.reachapp.models import SocialProfile
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
