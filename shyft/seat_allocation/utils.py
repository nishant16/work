import json

from seat_allocation.models import (Allocation,
                                    Room
                                    )

from django.db.models import Count, Q


# - Write a query to identify which room/seat was a student seated on a particular given date?

def get_student_room_bydate(date):
    """
    :param date: datetime object
    :return: queryset with values student name , seat_sid, room_name
    ex: <QuerySet [{'student__name': 'nishant', 'seat__sid': 'b1', 'seat__room__name': 'room_b'}]>
    """
    # as of now in param I am taking datetime object, if date string is passed need to add line
    # to convert string date by strptime method
    student_room_queryset = Allocation.objects.filter(Q(start_date=date) | Q(end_date=date)).\
        values("student__name", "seat__sid", "seat__room__name")
    return student_room_queryset

# Write a query to fetch the room ID in json format ({‘room_id’: XX}) for the room
# with the maximum number of seated people.


def get_max_student_in_room():
    """
    :return: room_id with maximum no. of student count
    """
    max_student_room = Room.objects.filter(seat__allocation__end_date__isnull=True)\
        .annotate(count=Count("seat__allocation__student__pk"))\
        .order_by("id").values("name", "count")\
        .order_by("count").last()

    max_room_data = json.dumps(max_student_room)
    return max_room_data
