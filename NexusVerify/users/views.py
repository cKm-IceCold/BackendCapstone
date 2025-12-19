from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from .services import assign_user_to_group

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        role = request.data.get("role", "Customer")
        assign_user_to_group(user, role)

        return Response(
            {"message": "User registered successfully"},
            status=201
        )


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "roles": list(user.groups.values_list("name", flat=True))
        })

# Create your views here.
