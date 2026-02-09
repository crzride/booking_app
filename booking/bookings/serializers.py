from django.db.models import Sum
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from bookings.models import Booking


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "room",
            "check_in",
            "check_out",
            "guest_number",
            "rooms_count",
        ]

    def validate(self, attrs):
        room = attrs["room"]
        rooms_count = attrs["rooms_count"]
        check_in = attrs["check_in"]
        check_out = attrs["check_out"]

        # Create UNSAVED Booking instance
        booking = Booking(
            room=room,
            rooms_count=rooms_count,
            check_in=check_in,
            check_out=check_out,
        )
       # Django model validation
        try:
            booking.full_clean()
        except DjangoValidationError as error:
            raise serializers.ValidationError(error.message_dict)

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

        if rooms_count > available_rooms:
            raise serializers.ValidationError(
                f"for the selected dates available only  {available_rooms}."
                f"Please change dates or choose another room type"
            )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        return Booking.objects.create(
            user=user,
            **validated_data
        )



