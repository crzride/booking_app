from rest_framework import serializers

from hotels.models import Hotel, Room


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('name', 'address', 'description',
                  'phone', 'owner', 'email')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('hotel', 'type', 'guest_number',
                  'price', 'stock', 'prepayment')


