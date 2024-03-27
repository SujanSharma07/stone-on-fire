# forms.py
from django import forms

from .models import Reservation


class ReservationForm(forms.ModelForm):
    message = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = Reservation
        fields = [
            "name",
            "phone",
            "customer_counts",
            "reservation_date",
            "reservation_time",
            "message",
        ]
