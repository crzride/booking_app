from django.db.models import Sum
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from bookings.models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "room",
            "rooms_count",
            "guest_number",
            "check_in",
            "check_out",
        ]

    def validate(self, attrs):
        room = attrs["room"]
        rooms_count = attrs["rooms_count"]
        check_in = attrs["check_in"]
        check_out = attrs["check_out"]
        guest_number = attrs["guest_number"]

        user = self.context["request"].user
        hotel = room.hotel

        # Create UNSAVED Booking instance
        booking = Booking(
            user=user,
            hotel=hotel,
            room=room,
            rooms_count=rooms_count,
            guest_number=guest_number,
            check_in=check_in,
            check_out=check_out,
        )
       # Django model validation
        try:
            booking.full_clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.message_dict)

        #Guest number check
        room_guest_number = room.guest_number
        if guest_number > room_guest_number:
            raise serializers.ValidationError(
                f"This room allows a maximum of {room_guest_number} guests."
            )

        # Availability check
        overlapping = Booking.objects.filter(
            room = room,
            check_in__lt=check_out,
            check_out__gt=check_in,
        )

        total_booked = overlapping.aggregate(
            total = Sum('rooms_count')
        )['total'] or 0

        available_rooms = room.stock - total_booked

        print(f"total_booked = {total_booked}")
        print(f"available_rooms = {available_rooms}")

        if available_rooms == 0:
            raise serializers.ValidationError(
                f"for the selected dates rooms are not available."
                f"Please change dates or choose another room type"
            )

        if rooms_count > available_rooms:
            raise serializers.ValidationError(
                f"for the selected dates available only  {available_rooms} rooms."
                f"Please change dates or choose another room type"
            )


        return attrs

    def create(self, validated_data):
        room = validated_data["room"]
        return Booking.objects.create(
            hotel=room.hotel,
            **validated_data
        )



class BookingListSerializer(serializers.ModelSerializer):
    hotel = serializers.StringRelatedField(read_only=True)
    room = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Booking
        fields = [
            "hotel",
            "user",
            "room",
            "rooms_count",
            "guest_number",
            "check_in",
            "check_out",
            "status",
            "created_at"
        ]


