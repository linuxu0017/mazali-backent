from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer

class AuthView(APIView):
    """
    Bitta class orqali Register, Login, Logout va Profile endpointlari
    'action' query parametri orqali aniqlanadi.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        action = request.query_params.get('action')
        
        # REGISTER
        if action == 'register':
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "user": serializer.data,
                    "token": token.key
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # LOGIN
        elif action == 'login':
            phone_number = request.data.get('phone_number')
            password = request.data.get('password')
            user = authenticate(phone_number=phone_number, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key})
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # LOGOUT
        elif action == 'logout':
            if not request.user.is_authenticated:
                return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
            request.user.auth_token.delete()
            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)

        # PROFILE
        elif action == 'profile':
            if not request.user.is_authenticated:
                return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = CustomUserSerializer(request.user)
            return Response(serializer.data)

        return Response({"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
