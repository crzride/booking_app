from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from hotels.models import Hotel, Room
from hotels.serializers import HotelSerializer, RoomSerializer


class HotelView(APIView):
    permission_classes = [IsAuthenticated]
#Required to replace it to ModelViewSet or whatever
    def get(self, request):
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        hotel = get_object_or_404(Hotel, pk=pk)
        serializer = HotelSerializer(hotel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RoomView(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['hotel']
    search_fields = ['name', 'author_name']
    ordering_fields = ['hotel', 'type', 'guest_number',
                  'price']
    permission_classes = [AllowAny]
