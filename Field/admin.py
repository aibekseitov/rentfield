from django.contrib import admin

# Register your models here.
from Field.models import Field, Image, Timetable

admin.site.register(Field)
admin.site.register(Image)
admin.site.register(Timetable)