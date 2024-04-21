from datetime import datetime, time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from main.models import Reservation

from .forms import ReservationForm


class DashboardView(TemplateView):
    template_name = "index.html"


@csrf_exempt
def reservation_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        form_data = request.POST.copy()

        # Transform the time format before validating the form
        form_data["reservation_time"] = transform_time_format(
            form_data["reservation_time"]
        )

        form = ReservationForm(form_data)

        if form.is_valid():
            # Transform the time format before saving to the model
            form.cleaned_data["reservation_time"] = transform_time_format(
                form.cleaned_data["reservation_time"]
            )

            # Save the form data to the model
            reservation = form.save()

            # Additional logic (e.g., sending email, etc.) can be added here
            return JsonResponse({"status": "success", "reservation_id": reservation.id})
        else:
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)

    # If the request method is not POST, return an error response
    return JsonResponse(
        {"status": "error", "message": "Invalid request method"}, status=405
    )


# Function to transform the time format
def transform_time_format(input_time):
    # Check if input_time is already a datetime.time object
    if isinstance(input_time, time):
        return input_time.strftime("%H:%M:%S")

    # Implement your logic to transform the time format here
    # For example, you can handle variations in input format
    try:
        # Attempt to parse the time with the original format
        transformed_time = datetime.strptime(str(input_time), "%I:%M%p").strftime(
            "%H:%M:%S"
        )
    except ValueError:
        try:
            # If the original format fails, try a different format
            transformed_time = datetime.strptime(str(input_time), "%I:%M %p").strftime(
                "%H:%M:%S"
            )
        except ValueError:
            # If both formats fail, raise an error or handle accordingly
            raise ValueError("Invalid time format")

    return transformed_time


@csrf_exempt
def available_times(request):
    reservation_date = request.GET["date"]
    available_times = Reservation.get_available_times(reservation_date=reservation_date)
    # booked_times = [reservation.time for reservation in reservations]
    # # Get all available times (replace with your logic)
    # available_times = ['10:00', '11:00', '12:00', ...]  # Replace with your time slots
    # # Filter out booked times from available times
    # available_times = [time for time in available_times if time not in booked_times]
    # return JsonResponse(available_times, safe=False)

    reservation_date = request.GET["date"]
    available_times = Reservation.get_available_times(reservation_date=reservation_date)
    return JsonResponse(available_times, safe=False)
