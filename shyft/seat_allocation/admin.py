from django.contrib import admin
from .models import Student, Room, Seat, Allocation


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["name", "email"]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = [
        "sid",
        "room",
    ]


@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ["student", "seat", "start_date", "end_date"]
