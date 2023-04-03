from django.core.serializers.json import Serializer


class CourseSerializer(Serializer):

    def get_dump_object(self, obj):
        data = {'fields': self._current}
        return data
