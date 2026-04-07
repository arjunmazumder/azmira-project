from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from .models import User

# ১. রেজিস্ট্রেশন ভিউ
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Fetched all requests",
                "data": {
                    "requests": [UserSerializer(user).data]
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "message": "Fetched all requests",
            "data": {"requests": [serializer.errors]}
        }, status=status.HTTP_400_BAD_REQUEST)

# ২. লগইন ভিউ (JWT)
class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                "message": "Fetched all requests",
                "data": {
                    "requests": [{
                        "access": response.data['access'],
                        "refresh": response.data['refresh'],
                        "status": "Login Successful"
                    }]
                }
            }, status=status.HTTP_200_OK)
        return response

# ৩. প্রোফাইল ভিউ
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            "message": "Fetched all requests",
            "data": {
                "requests": [serializer.data]
            }
        }, status=status.HTTP_200_OK)