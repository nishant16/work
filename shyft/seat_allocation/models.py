import datetime

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Student(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return "%s" % self.name


class Room(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return "%s" % self.name


class Seat(TimeStampedModel):
    sid = models.CharField(max_length=10, unique=True)  # a1, a2... for Room A, b1,b2.... for Room B
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.sid, self.room.name)


class Allocation(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    start_date = models.DateField("Start Date", default=timezone.now, null=True, blank=True)
    end_date = models.DateField("End Date", null=True, blank=True)

    def __str__(self):
        return "%s %s" % (self.seat, self.student.name)

    class Meta:
        verbose_name = "Allocation"
        verbose_name_plural = "Allocations"

    def clean(self, *args, **kwargs):
        seat = self.seat
        student = self.student

        # if seat is occupied , no other student will allocate that seat
        allocation_exists = Allocation.objects.filter(seat=seat, end_date__isnull=True).exists()
        if allocation_exists:
            raise ValidationError('Allocation already exists for this room/seat')

        # student can not change their seat in more than one room/seat on a given date.
        student_allocation_exists = Allocation.objects.filter(
            student=student, start_date=self.start_date
        ).exists()
        if student_allocation_exists:
            raise ValidationError(
                'Student can not be seated in more than one room/seat on a given date'
            )
        try:
            # student is already seated in any room/seat and want to change the room/seat
            allocation = Allocation.objects.get(
                student=student, end_date__isnull=True
            )
            # we save existing allocation of student with end date to historical data.
            yesterday_date = timezone.now() - datetime.timedelta(days=1)
            allocation.end_date = yesterday_date
            allocation.save()
            # after save existing alloacation , new allocation provided to the student
        except Allocation.DoesNotExist:
            # new student doesn't have any previous record, new allocation provided to the student
            pass

