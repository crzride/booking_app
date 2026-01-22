from datetime import date, timedelta

from django.db import models
from django.db.models import ManyToManyField, ForeignKey, PROTECT

from hotels.models import Hotel, Room
from users.models import User


def tomorrow():
    return date.today() + timedelta(days=1)


class Booking(models.Model):
    user = ForeignKey(User, on_delete=models.PROTECT, related_name='bookings')
    hotel = ForeignKey(Hotel, on_delete=models.PROTECT, related_name='bookings')
    room = ManyToManyField(Room, related_name='bookings')
    check_in = models.DateField(default=date.today)
    check_out = models.DateField(default=tomorrow)
