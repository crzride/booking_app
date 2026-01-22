from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
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
    guest_number = models.PositiveIntegerField(default=1,
                                               validators=[
                                                 MaxValueValidator(10)
                                               ])
    check_in = models.DateField(default=date.today)
    check_out = models.DateField(default=tomorrow)

    def clean(self):
        today = date.today()

        if self.check_in < today:
            raise ValidationError({
                "check_in": "Check-in must be today or later."
            })

        if self.check_out < tomorrow():
            raise ValidationError({
                "check_out": "Check-out must be tomorrow or later."
            })

        if self.check_out <= self.check_in:
            raise ValidationError({
                "check_out": "Check-out must be after check-in."
            })


    def __str__(self):
        return f"{self.user} {self.hotel} id {self.id}"