from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer, PasswordChangeSerializer


class RegisterView (CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data = request.data,
            context = {"request": request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK
        )

