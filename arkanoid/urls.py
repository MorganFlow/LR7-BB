"""
URL configuration for arkanoid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from game.views import register, login, UserProfileView, GameSessionViewSet, LeaderboardViewSet, AchievementViewSet, load_latest_session
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'game-sessions', GameSessionViewSet)
router.register(r'leaderboard', LeaderboardViewSet)
router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register),
    path('api/login/', login),
    path('api/profile/', UserProfileView.as_view()),
    path('api/load-session/', load_latest_session),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)