from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

import pytz

my_tz = pytz.timezone('Asia/Almaty')

class FieldManager(models.Manager):
    def only_active(self):
        return super(FieldManager,self).get_queryset().filter(status=Field.Statuses.ACTIVE)

class Field(models.Model):
    class Types:
        HOVERED = 1
        NOT_HOVERED = 0

    class Statuses:
        ACTIVE = 1
        NOT_ACTIVE = 0

    class Games:
        Football = 0
        Basketball = 1
        Tennis = 2

    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, related_name='owner')
    game = models.IntegerField()

    hovered = models.IntegerField(default=Types.NOT_HOVERED)
    status = models.IntegerField(default=Statuses.ACTIVE)
    description = models.CharField(max_length=500,blank=True)
    price = models.IntegerField(null=True)
    width = models.CharField(max_length=20)
    length = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20, blank=True)
    likes = models.IntegerField(default=0)

    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True,null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True,null=True)


    objects = FieldManager()

    @property
    def area(self):
        return self.width + 'x' + self.length

    def __str__(self):
        return ' - '.join([str(self.id),self.name,self.area,str(self.price)])



def field_image_directory(instance, filename):
    return 'static/field_images/%s/%s' % (instance.field.id, filename)

class Image(models.Model):
    field = models.ForeignKey(Field, related_name='images',default=None)
    image = models.ImageField(upload_to=field_image_directory,verbose_name='Image')

    def __str__(self):
        return ' - '.join([self.field.name,str(self.id)])


class TimetableManager(models.Manager):
    def booked(self, request):
        date = datetime.strptime(request.GET['date'], "%d-%m-%y")

        return super(TimetableManager, self).get_queryset().filter(Q(start_time__year=date.year,
                                                                   start_time__month=date.month,
                                                                   start_time__day=date.day) | Q(end_time__year=date.year,
                                                                                                 end_time__month=date.month,
                                                                                                 end_time__day=date.day))

class Timetable(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = TimetableManager()

    def __str__(self):
        return ' - '.join([str(self.field), str(self.user), self.start_time.strftime('%B %d'),self.start_time.strftime('%H:%M'), self.end_time.strftime('%H:%M')])

class UserLikes(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

'''
    https://www.tutorialspoint.com/python/time_strptime.htm
    Time format
'''