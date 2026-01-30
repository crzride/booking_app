from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from hotels.models import Hotel
from hotels.serializers import HotelSerializer


class HotelView(APIView):

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


