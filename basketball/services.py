import pandas as pd
import numpy as np
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet, Avg, Max, Min

from . import models
from .models import Player, Lineup, ShotPrediction, LineupPlayersPrediction, LineupStatisticsPrediction, \
    LineupsModelRating

User = get_user_model()


class ProfileService():
    def create(self, user: User):
        profile = models.Profile.objects.create(user=user)
        profile.save()


class PlayerService:
    def create_and_save_player_from_csv(self, player):
        p = Player(
            player_id=player['PLAYER_ID'],
            player_name=player['PLAYER_NAME'],
            team_id=player['TEAM_ID'],
            team_abr=player['TEAM_ABBREVIATION'],
            age=int(float(player['AGE'])),
            games_played=player['GP'],
            w=player['W'],
            l=player['L'],
            w_pct=player['W_PCT'],
            min=player['MIN'],
            e_off_rating=player['E_OFF_RATING'],
            off_rating=player['OFF_RATING'],
            e_def_rating=player['E_DEF_RATING'],
            def_rating=player['DEF_RATING'],
            e_net_rating=player['E_NET_RATING'],
            net_rating=player['NET_RATING'],
            ast_pct=player['AST_PCT'],
            ast_to=player['AST_TO'],
            ast_ratio=player['AST_RATIO'],
            oreb_pct=player['OREB_PCT'],
            dreb_pct=player['DREB_PCT'],
            reb_pct=player['REB_PCT'],
            tm_tov_pct=player['TM_TOV_PCT'],
            e_tov_pct=player['E_TOV_PCT'],
            efg_pct=player['EFG_PCT'],
            ts_pct=player['TS_PCT'],
            usg_pct=player['USG_PCT'],
            e_usg_pct=player['E_USG_PCT'],
            e_pace=player['E_PACE'],
            pace=player['PACE'],
            pace_per40=player['PACE_PER40'],
            pie=player['PIE'],
            poss=player['POSS'],
            fgm=player['FGM'],
            fga=player['FGA'],
            fgm_pg=player['FGM_PG'],
            fga_pg=player['FGA_PG'],
            fg_pct=player['FG_PCT'])
        p.save()

    def delete_all_players(self):
        Player.objects.all().delete()

    def players_filter_search(self, **kwargs) -> QuerySet:
        players = models.Player.objects.all()
        filters = {key: val for key, val in kwargs.items() if val}
        return players.filter(**filters)

    def get_all_players_names(self):
        choices = [('', '-- Jugador --')]
        players_names = models.Player.objects.values_list('player_name', flat=True).order_by('player_name')
        for player in players_names:
            choices.append((player, player))

        return choices

    def find_player_by_id(self, player_id: str) -> Player:
        player = models.Player.objects.get(player_id=player_id)
        return player

    def find_players_by_team_id(self, team_id: str) -> QuerySet:
        players = models.Player.objects.filter(team_id=team_id)
        return players


class LineupService:
    def create_and_save_lineup_from_csv(self, lineup):
        quinteto = Lineup(
            group_set=lineup['GROUP_SET'],
            group_id=lineup['GROUP_ID'],
            group_name=lineup['GROUP_NAME'],
            team_id=lineup['TEAM_ID'],
            team_abreviation=lineup['TEAM_ABBREVIATION'],
            games_played=lineup['GP'],
            w=lineup['W'],
            l=lineup['L'],
            w_pct=lineup['W_PCT'],
            min=lineup['MIN'],
            e_off_rating=lineup['E_OFF_RATING'],
            off_rating=lineup['OFF_RATING'],
            e_def_rating=lineup['E_DEF_RATING'],
            def_rating=lineup['DEF_RATING'],
            e_net_rating=lineup['E_NET_RATING'],
            net_rating=lineup['NET_RATING'],
            ast_pct=lineup['AST_PCT'],
            ast_to=lineup['AST_TO'],
            ast_ratio=lineup['AST_RATIO'],
            oreb_pct=lineup['OREB_PCT'],
            dreb_pct=lineup['DREB_PCT'],
            reb_pct=lineup['REB_PCT'],
            tm_tov_pct=lineup['TM_TOV_PCT'],
            efg_pct=lineup['EFG_PCT'],
            ts_pct=lineup['TS_PCT'],
            e_pace=lineup['E_PACE'],
            pace=lineup['PACE'],
            pace_per40=lineup['PACE_PER40'],
            poss=lineup['POSS'],
            pie=lineup['PIE'])
        quinteto.save()

    def delete_all_lineups(self):
        Lineup.objects.all().delete()

    def lineups_filter_search(self, **kwargs) -> QuerySet:
        lineups = models.Lineup.objects.all()
        filters = {key: val for key, val in kwargs.items() if val}
        return lineups.filter(**filters)


class ShotPredictionService:
    def create(self, player, home_score, away_score, time, is_home, time_played,
               points_scored, created_by: User, solucion, probabilidad):
        shot_prediction = ShotPrediction(player=player, home_score=home_score, away_score=away_score, time=time,
                                         is_home=is_home, time_played=time_played, points_scored=points_scored,
                                         created_by=created_by, solucion=solucion, probabilidad=probabilidad)
        shot_prediction.save()

    def my_predictions(self, user: User) -> QuerySet:
        predictions = models.ShotPrediction.objects.filter(
            created_by=user)
        return predictions


class LineupPredictionByPlayersService:
    def statistics_5_players(self, nameplayer1, nameplayer2, nameplayer3, nameplayer4, nameplayer5):

        for player in Player.objects.all():
            if player.player_name == nameplayer1:
                player1 = player
            elif player.player_name == nameplayer2:
                player2 = player
            elif player.player_name == nameplayer3:
                player3 = player
            elif player.player_name == nameplayer4:
                player4 = player
            elif player.player_name == nameplayer5:
                player5 = player

        result = pd.DataFrame(
            np.c_[player1.efg_pct, player2.efg_pct, player3.efg_pct, player4.efg_pct, player5.efg_pct,
                  player1.ts_pct, player2.ts_pct, player3.ts_pct, player4.ts_pct, player5.ts_pct,
                  player1.pie, player2.pie, player3.pie, player4.pie, player5.pie],
            columns=['EFGJ1', 'EFGJ2', 'EFGJ3', 'EFGJ4', 'EFGJ5',
                     'TSJ1', 'TSJ2', 'TSJ3', 'TSJ4', 'TSJ5',
                     'PIEJ1', 'PIEJ2', 'PIEJ3', 'PIEJ4', 'PIEJ5'])

        return result

    def create(self, player1, player2, player3, player4, player5, off_rating, created_by):
        lineup_prediction = LineupPlayersPrediction(player1=player1, player2=player2, player3=player3, player4=player4,
                                                    player5=player5, off_rating=float(off_rating),
                                                    created_by=created_by)
        lineup_prediction.save()

    def my_predictions(self, user: User) -> QuerySet:
        predictions = models.LineupPlayersPrediction.objects.filter(
            created_by=user)
        return predictions

    def my_best_predictions(self, user: User) -> QuerySet:
        predictions = models.LineupPlayersPrediction.objects.filter(
            created_by=user).order_by('-off_rating')[:10]
        return predictions

    def my_last_predictions(self, user: User) -> QuerySet:
        predictions = models.LineupPlayersPrediction.objects.filter(
            created_by=user).order_by('-created_at')[:10]
        return predictions



class LineupPredictionByStatisticsService:
    def create(self, efg_pct, ts_pct, pie, off_rating, created_by):
        lineup_prediction = LineupStatisticsPrediction(efg_pct=float(efg_pct), ts_pct=float(ts_pct), pie=float(pie),
                                                       off_rating=float(off_rating), created_by=created_by)
        lineup_prediction.save()

    def my_predictions(self, user: User) -> QuerySet:
        predictions = models.LineupStatisticsPrediction.objects.filter(
            created_by=user)
        return predictions

    def my_best_predictions(self, user: User) -> QuerySet:
        predictions = models.LineupStatisticsPrediction.objects.filter(
            created_by=user).order_by('-off_rating')[:10]
        return predictions

    def my_last_predictions(self, user: User) -> QuerySet:
        predictions = models.LineupStatisticsPrediction.objects.filter(
            created_by=user).order_by('-created_at')[:10]
        return predictions


class LineupsModelRatingService:
    def get_last(self):
        lineup_model_rating = models.LineupsModelRating.objects.order_by('-created_at').first()
        return lineup_model_rating
    def create_statistics(self, created_by):
        max_off_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Max('off_rating'))
        min_off_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Min('off_rating'))
        avg_off_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Avg('off_rating'))

        max_def_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Max('def_rating'))
        min_def_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Min('def_rating'))
        avg_def_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Avg('def_rating'))

        max_net_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Max('net_rating'))
        min_net_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Min('net_rating'))
        avg_net_rating = models.Lineup.objects.filter(min__gte=30).aggregate(Avg('net_rating'))

        lineup_model_rating = LineupsModelRating(max_off_rating=max_off_rating['off_rating__max'], min_off_rating=min_off_rating['off_rating__min'],
                                                 avg_off_rating=avg_off_rating['off_rating__avg'], max_def_rating=max_def_rating['def_rating__max'],
                                                 min_def_rating=min_def_rating['def_rating__min'], avg_def_rating=avg_def_rating['def_rating__avg'],
                                                 max_net_rating=max_net_rating['net_rating__max'], min_net_rating=min_net_rating['net_rating__min'],
                                                 avg_net_rating=avg_net_rating['net_rating__avg'], created_by=created_by)
        lineup_model_rating.save()
