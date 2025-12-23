from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import UserProfile, GameSession, Leaderboard, Achievement

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'date_of_birth')

@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'level', 'time_played', 'is_completed')
    actions = ['export_to_xlsx']

    def export_to_xlsx(self, request, queryset):
        wb = Workbook()
        ws = wb.active
        ws.append(['User', 'Score', 'Level', 'Time Played', 'Completed', 'Created At'])
        for session in queryset:
            ws.append([session.user.username, session.score, session.level, str(session.time_played), session.is_completed, session.created_at])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=game_sessions.xlsx'
        wb.save(response)
        return response

    export_to_xlsx.short_description = "Export selected to XLSX"

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'rank', 'date_achieved')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'achieved_at')
    # Админ может добавлять достижения вручную