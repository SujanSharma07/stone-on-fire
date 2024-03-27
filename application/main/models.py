from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.

tz = timezone.get_current_timezone()

AVAILABLE_TIMESLOTS = {
    "11:00AM",
    "12:00PM",
    "01:00PM",
    "02:00PM",
    "03:00PM",
    "04:00PM",
    "05:00PM",
}


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(
        _("created on"), help_text=_("Object created date and time"), auto_now_add=True
    )
    modified_on = models.DateTimeField(
        _("modified on"), help_text=_("Object modified date and time"), auto_now=True
    )
    created_on_np_date = models.DateField(
        editable=False, db_index=True, default=timezone.localdate
    )

    class Meta:
        abstract = True

    @classmethod
    def new(cls, **kwargs):
        return cls.objects.create(**kwargs)

    def update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        self.save()
        return self

    def delete(self, force_delete=True, **kwargs):
        if force_delete:
            super().delete(**kwargs)
        else:
            self.update(is_obsolete=True)
            return self


class BaseModel(TimeStampedModel):
    """
    Soft delete model
    """

    deleted_on = models.DateTimeField(
        _("deleted on"),
        null=True,
        default=None,
        blank=True,
        help_text=_("Object deleted date and time"),
    )
    is_obsolete = models.BooleanField(
        _("is obsolete"), default=False, help_text=_("Is the object deleted?")
    )
    meta = models.JSONField(default=dict, null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, force_delete=True, **kwargs):
        if force_delete:
            super().delete(**kwargs)
        else:
            self.update(is_obsolete=True, deleted_on=timezone.now())
            return self


class Reservation(BaseModel):
    REQUESTED = "Requested"
    CONFIRM = "Confirm"
    CANCLED = "Cancled"
    COMPLETED = "Completed"

    STATUS_CHOICES = [
        (REQUESTED, REQUESTED),
        (CONFIRM, CONFIRM),
        (CANCLED, CANCLED),
        (COMPLETED, COMPLETED),
    ]
    name = models.CharField(max_length=255, help_text="Customers full name")

    email = models.EmailField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )
    phone = models.CharField(
        max_length=13, db_index=True, help_text="Contact number for the customer"
    )
    reservation_date = models.DateField(help_text="Date of reservation")
    reservation_time = models.TimeField(auto_now=False, auto_now_add=False)

    customer_counts = models.PositiveIntegerField(
        help_text="Number of Customers for the table"
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=25, default=REQUESTED)
    message = models.TextField()

    def __str__(self):
        return f"{self.reservation_date} - {self.name}"

    @classmethod
    def get_available_times(cls, reservation_date):
        t_reservations = list(
            cls.objects.filter(reservation_date=reservation_date)
            .only("reservation_time")
            .values_list("reservation_time")
        )
        if t_reservations.exists():
            # Convert each datetime.time object in the list
            not_available_time = [
                convert_to_12_hour_format(time[0]) for time in t_reservations
            ]
            return AVAILABLE_TIMESLOTS - not_available_time

        return AVAILABLE_TIMESLOTS


# Function to convert datetime.time to string in "08:00am" format
def convert_to_12_hour_format(time_obj):
    return time_obj.strftime("%I:%M%p")


# class subscriber(BaseModel):
