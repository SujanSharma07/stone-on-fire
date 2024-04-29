from django.urls import path

from .views import DashboardView, available_times, reservation_view

urlpatterns = [
    path("", DashboardView.as_view(), name="home"),
    path("reservation/", reservation_view, name="reservation"),
    path("reservations/available_times/", available_times, name="available_times"),
]
