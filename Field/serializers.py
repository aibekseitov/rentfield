from rest_framework.serializers import ModelSerializer
from Field.models import Field, Image, Timetable


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class FieldReadSerializer(ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    class Meta:
        model = Field
        fields = '__all__'

class FieldWriteSerializer(ModelSerializer):
    class Meta:
        model = Field
        fields = ('owner','name','hovered','price','width','length','address','game','phone_number','longitude', 'latitude')


class TimetableSerializer(ModelSerializer):
    class Meta:
        model = Timetable
        fields = '__all__'
