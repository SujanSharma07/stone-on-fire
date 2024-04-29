# forms.py
from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    customer_message = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Reservation
        fields = [
            "customer_name",
            "customer_phone",
            "customer_email",
            "customer_counts",
            "reservation_date",
            "reservation_time",
            "customer_message",
        ]
