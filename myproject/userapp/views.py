from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .models import CustomUser
from .serializers import UserSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # default

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [ IsAuthenticated,IsOwnerOrAdmin]

        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

class GetProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    
class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # this adds the token to the blacklist

            return Response({"msg": "Token blacklisted successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)