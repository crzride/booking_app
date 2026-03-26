from logging import raiseExceptions

from  rest_framework.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from bookings.models import Booking
from bookings.serializers import BookingCreateSerializer, BookingListSerializer
from hotels.models import Room


class BookingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer

        return BookingListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data["room"]
        check_in = serializer.validated_data["check_in"]
        check_out = serializer.validated_data["check_out"]
        rooms_count = serializer.validated_data["rooms_count"]

        with transaction.atomic():
             # lock room
            room = Room.objects.select_for_update().get(id=room.id)

            overlapping = Booking.objects.filter(
                room=room,
                check_in__lt=check_out,
                check_out__gt=check_in,
            )

            total_booked = overlapping.aggregate(
                total=Sum('rooms_count')
            )['total'] or 0

            available_rooms = room.stock - total_booked

            if available_rooms == 0:
                raise ValidationError(
                    f"for the selected dates rooms are not available."
                    f"Please change dates or choose another room type"
                )

            if rooms_count > available_rooms:
                raise ValidationError(
                    f"for the selected dates available only  {available_rooms} rooms."
                    f"Please change dates or choose another room type"
                )

            booking = serializer.save(user=request.user)
            print(f"total_booked = {total_booked}")
            print(f"available_rooms = {available_rooms}")

        return Response(
            BookingListSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )
