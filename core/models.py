from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape  # Для защиты от XSS

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, max_length=500)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def clean(self):
        self.bio = escape(self.bio)  # Экранирование от XSS

class GameSession(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_state = models.JSONField()  # JSON для сохранения состояния (уровень, очки и т.д.)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    time_played = models.DurationField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Level {self.level}"

class Leaderboard(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    rank = models.IntegerField()
    date_achieved = models.DateTimeField(auto_now_add=True)
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])

    class Meta:
        ordering = ['-score']

    def __str__(self):
        return f"{self.user.username} - {self.score}"

class Achievement(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    name = models.CharField(max_length=100)
    description = models.TextField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} for {self.user.username}"