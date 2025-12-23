from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile, GameSession, Leaderboard, Achievement
from .serializers import UserProfileSerializer, GameSessionSerializer, LeaderboardSerializer, AchievementSerializer
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Регистрация
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username exists'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username, email, password)
    UserProfile.objects.create(user=user)
    refresh = RefreshToken.for_user(user)
    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})

# Логин
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Профиль
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(UserProfile, user=self.request.user)

# Сессии игры
class GameSessionViewSet(viewsets.ModelViewSet):
    serializer_class = GameSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GameSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Последнее сохранение
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def load_latest_session(request):
    session = GameSession.objects.filter(user=request.user).order_by('-created_at').first()
    if session:
        return Response(GameSessionSerializer(session).data)
    return Response({'error': 'No session found'}, status=status.HTTP_404_NOT_FOUND)

# Лидерборд
class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.AllowAny]  # Гости могут смотреть

    def get_queryset(self):
        queryset = Leaderboard.objects.all()
        difficulty = self.request.query_params.get('difficulty')
        date_from = self.request.query_params.get('date_from')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if date_from:
            queryset = queryset.filter(date_achieved__gte=date_from)
        return queryset

# Достижения
class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)