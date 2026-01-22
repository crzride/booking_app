from django.core.validators import MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Hotel(models.Model):
    name = models.CharField(max_length=50, blank=False)
    address = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=False)
    phone = PhoneNumberField (region=None,blank=True,null=True)
    owner = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True, blank=False)

    def __str__(self):
        return f"Hotel {self.name}"


class Room(models.Model):
    ROOM_TYPES = (
        ('ST_DOUBLE', 'Standard Double Room'),
        ('DLX_DOUBLE', 'Delux Double Room'),
        ('SUITE', 'Suite with a Balcony'),
        ('TWIN', 'Twin Room'),
        ('FAMILY', 'Family Studio')
    )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    type = models.CharField(choices=ROOM_TYPES, max_length=30)
    guest_number = models.PositiveIntegerField(default=1,
                                               validators=[
                                                 MaxValueValidator(6)
                                               ])
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    prepayment = models.BooleanField(default=False)
#     there is a question how to set prepayment)

    def __str__(self):
        return f"{self.hotel} {self.type} id {self.id}"




