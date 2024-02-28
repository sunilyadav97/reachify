from django.urls import path
from django.views.generic import TemplateView
from reachify.reachapp.views import HomeView, DashboardView, platform_engagement_credits_view, AddPromotionView, \
    PromotionListView

app_name = 'reachapp'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("add/promotion/", AddPromotionView.as_view(), name="add_promotion"),
    path('promotions', PromotionListView.as_view(), name="promotion_list"),
    path(
        'fetch/platform-engagement/<int:id>/credtis',
        platform_engagement_credits_view,
        name="platform_engagement_credits"
    ),
]
