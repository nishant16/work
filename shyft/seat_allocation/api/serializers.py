from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField)

from seat_allocation.models import (Allocation,
                                    Room
                                    )


class RoomSerializer(ModelSerializer):
    """
    room serializer
    """
    student_list_in_class = SerializerMethodField()

    class Meta:
        model = Room
        fields = [
            'student_list_in_class',
        ]

    def get_student_list_in_class(self, classrroom_obj):
        """
        List of students currently seated in a given classroom
        :param: classroom_obj
        :return: student name list in a given class
        """
        student_list = Allocation.objects.filter(
            seat__room_id=classrroom_obj.id, end_date__isnull=True
        ).values_list("student__name", flat=True)
        return student_list


class AllocationSerializer(ModelSerializer):
    """
    allocation serializer
    """

    class Meta:
        model = Allocation
        fields = '__all__'
