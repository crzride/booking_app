from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from bookings.models import Booking
from bookings.serializers import BookingCreateSerializer, BookingListSerializer


class BookingViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return BookingCreateSerializer

        return BookingListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)