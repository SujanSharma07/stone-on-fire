import csv

from django.contrib import admin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone

from main.models import Reservation

# Register your models here.


class BaseAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export Selected"


class NoCountPaginator(Paginator):
    @property
    def count(self):
        return 999999999  # Some arbitrarily large number, so we can still get our page tab.


class CustomModelAdmin(admin.ModelAdmin):
    use_date_range = False
    show_date_filter = False
    possible_readonly_fields = ["created_on", "modified_on", "deleted_on"]
    possible_raw_id_fields = [
        "product",
    ]
    paginator = NoCountPaginator

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.raw_id_fields = self.get_raw_id_fields(model)

    def get_readonly_fields(self, request, obj):
        readonly_fields = list(self.readonly_fields)
        for x in filter(lambda x: hasattr(obj, x), self.possible_readonly_fields):
            readonly_fields.append(x)
        return list(set(readonly_fields))

    def get_raw_id_fields(self, model):
        raw_id_fields = list(self.raw_id_fields)
        for x in filter(lambda x: hasattr(model, x), self.possible_raw_id_fields):
            raw_id_fields.append(x)
        return list(set(raw_id_fields))

    def get_exclude(self, request, obj):
        return self.possible_readonly_fields

    def serialize_model(self, to_state):
        to_state_serialized = {}
        for key, value in to_state.items():
            to_state_serialized[key] = str(value)
        return to_state_serialized

    def model_specs(self, request, obj, form, change):
        if obj.pk is None:
            if hasattr(obj, "created_by_id") and obj.created_by_id is None:
                obj.created_by_id = request.user.id
            if hasattr(obj, "performed_by_id") and obj.performed_by_id is None:
                obj.performed_by_id = request.user.id

        if obj.is_obsolete is True and any(
            [obj.deleted_on is None, obj.is_obsolete == ""]
        ):
            obj.deleted_on = timezone.now()
        obj.save()

    list_per_page = 50


class CustomReadonlyAdmin(CustomModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CustomCreateOnlyAdmin(CustomModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class CustomUpdateOnlyAdmin(CustomModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False


@admin.register(Reservation)
class AdvertisementAdmin(CustomModelAdmin):
    list_display = ("name", "reservation_date", "reservation_time")
    list_filter = ("created_on_np_date", "reservation_date", "reservation_time")
    search_fields = ("name",)
    ignore_fields = [""]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser and request.user.is_active:
            return ["created_on", "modified_on", "created_on_np_date"]
        return [f.name for f in self.model._meta.fields]

    def save_model(self, request, obj, form, change):
        obj.save()
