from django.contrib import admin

# Register your models here.
from . import models


class PlayerAdmin(admin.ModelAdmin):
    search_fields = ('player_id', 'player_name', 'age', 'team_id', 'team_abr')
    list_display = ('player_id', 'player_name', 'age', 'team_id', 'team_abr')


class LineupAdmin(admin.ModelAdmin):
    search_fields = ('group_id', 'group_name', 'team_id', 'team_abreviation')
    list_display = ('group_id', 'group_name', 'team_id', 'team_abreviation')


class ShotPredictionAdmin(admin.ModelAdmin):
    list_display = ('player', 'solucion', 'probabilidad', 'created_at', 'created_by')
    search_fields = ('player', 'created_by')


class LineupStatisticsPredictionAdmin(admin.ModelAdmin):
    search_fields = ('created_by',)
    list_display = ('efg_pct', 'ts_pct', 'pie', 'off_rating', 'created_at', 'created_by')


class LineupPlayersPredictionAdmin(admin.ModelAdmin):
    search_fields = ('player1', 'player2', 'player3', 'player4', 'player5', 'created_by')
    list_display = ('player1', 'player2', 'player3', 'player4', 'player5', 'off_rating', 'created_at', 'created_by')


class LineupsModelRatingAdmin(admin.ModelAdmin):
    list_display = (
        'max_off_rating', 'min_off_rating', 'avg_off_rating', 'max_def_rating', 'min_def_rating', 'avg_def_rating',
        'max_net_rating', 'min_net_rating', 'avg_net_rating', 'created_at')


admin.site.register(models.Profile)
admin.site.register(models.LineupsModelRating, LineupsModelRatingAdmin)
admin.site.register(models.ShotPrediction, ShotPredictionAdmin)
admin.site.register(models.LineupStatisticsPrediction, LineupStatisticsPredictionAdmin)
admin.site.register(models.LineupPlayersPrediction, LineupPlayersPredictionAdmin)
admin.site.register(models.Lineup, LineupAdmin)
admin.site.register(models.Player, PlayerAdmin)
