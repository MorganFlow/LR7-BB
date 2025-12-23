from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    SaveGameView, LoadGameView,
    LeaderboardView, UserAchievementsView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('game/save/', SaveGameView.as_view(), name='save_game'),
    path('game/load/', LoadGameView.as_view(), name='load_game'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('achievements/', UserAchievementsView.as_view(), name='achievements'),
]