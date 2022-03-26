from django.db.models import Count
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from seat_allocation.api.serializers import *
from seat_allocation.models import (Allocation,
                                    Room,
                                    Seat,
                                    Student
                                    )


class RoomViewset(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    @action(methods=['get'], detail=False)
    def student_list(self, request, *args, **kwargs):
        """
        List of students currently seated in a given classroom
        param: room_id
        """
        class_room_id = self.request.GET.get('room_id')
        try:
            class_room_obj = Room.objects.get(id=class_room_id)
            serializer = RoomSerializer(class_room_obj)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        except Room.DoesNotExist:
            data = {
                "detail": "Class room id not found %s" % class_room_id
            }
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['get'], detail=False)
    def classroom_list(self, request, *args, **kwargs):
        """
        List of classrooms with at least x students seated in them.
        :params: min_students
        """
        min_students = self.request.GET.get('min_students')
        if not min_students:
            min_students = 15
        room_list = list(Room.objects.filter(seat__allocation__end_date__isnull=True).
                         annotate(count=Count("seat__allocation__student__pk")).
                         order_by("id").filter(count__gte=min_students)
                         .values_list("name", flat=True)
                         )
        data = {
            'room_list_data': room_list
        }
        return Response(
            data,
            status=status.HTTP_200_OK
        )


class AllocationViewset(viewsets.ModelViewSet):
    serializer_class = AllocationSerializer
    queryset = Allocation.objects.all()

    @action(methods=['get'], detail=False)
    def change_student_room(self, request, *args, **kwargs):
        """
        Change the room of a student from Room A to Room B.
        :params: student_id
        """
        student_id = self.request.GET.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            data = {
                "detail": "Student id is not found %s" % student_id
            }
            return Response(
                data,
                status=status.HTTP_400_BAD_REQUEST
            )
        # room B is having id=2 as of now.
        room_b = Room.objects.get(id=2)
        seat_id = room_b.seat_set.filter(
            allocation__start_date__isnull=True
        ).values_list("sid", flat=True).first()
        seat = Seat.objects.get(sid=seat_id)
        # During new allocation clean method in models will save the end date for given student
        # given room a and then create a new entry
        Allocation.objects.create(student=student, start_date=timezone.now(), seat=seat)
        data = {
            'details': "Student Room changed successfully"
        }
        return Response(
            data,
            status=status.HTTP_200_OK
        )
