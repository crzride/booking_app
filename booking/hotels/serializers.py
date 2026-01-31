from rest_framework import serializers

from hotels.models import Hotel, Room


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('__all__')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('hotel', 'type', 'guest_number',
                  'price', 'quantity', 'prepayment')
