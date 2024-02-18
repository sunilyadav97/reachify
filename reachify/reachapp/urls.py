from django.urls import path
from django.views.generic import TemplateView
from reachify.reachapp.views import HomeView, DashboardView

app_name = 'reachapp'

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
]
