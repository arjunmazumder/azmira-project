from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RegisterSerializer, UserSerializer
from .models import User


# ✅ Register
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Registration successful",
                "data": {
                    "requests": [UserSerializer(user).data]
                }
            }, status=status.HTTP_201_CREATED)

        return Response({
            "message": "Registration failed",
            "data": {"requests": [serializer.errors]}
        }, status=status.HTTP_400_BAD_REQUEST)


# ✅ Login (JWT)
class CustomLoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            return Response({
                "message": "Login successful",
                "data": {
                    "requests": [{
                        "access": response.data['access'],
                        "refresh": response.data['refresh']
                    }]
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Login failed",
            "data": {"requests": [response.data]}
        }, status=status.HTTP_400_BAD_REQUEST)


# ✅ Profile View (GET + UPDATE)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    # Get Profile
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "message": "Profile fetched successfully",
            "data": {
                "requests": [serializer.data]
            }
        }, status=status.HTTP_200_OK)

    # Update Profile
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": {
                    "requests": [serializer.data]
                }
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Profile update failed",
            "data": {"requests": [serializer.errors]}
        }, status=status.HTTP_400_BAD_REQUEST)