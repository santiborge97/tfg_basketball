from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now

User = get_user_model()


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return self.user.username + ' profile'


class Lineup(models.Model):
    group_set = models.CharField(max_length=250)
    group_id = models.CharField(max_length=250, unique=True)
    group_name = models.CharField(max_length=250)
    team_id = models.CharField(max_length=250)
    team_abreviation = models.CharField(max_length=250)
    games_played = models.PositiveSmallIntegerField()
    w = models.PositiveSmallIntegerField()
    l = models.PositiveSmallIntegerField()
    w_pct = models.DecimalField(max_digits=6, decimal_places=3)
    min = models.DecimalField(max_digits=6, decimal_places=3)
    e_off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    e_def_rating = models.DecimalField(max_digits=6, decimal_places=3)
    def_rating = models.DecimalField(max_digits=6, decimal_places=3)
    e_net_rating = models.DecimalField(max_digits=6, decimal_places=3)
    net_rating = models.DecimalField(max_digits=6, decimal_places=3)
    ast_pct = models.DecimalField(max_digits=6, decimal_places=3)
    ast_to = models.DecimalField(max_digits=6, decimal_places=3)
    ast_ratio = models.DecimalField(max_digits=6, decimal_places=3)
    oreb_pct = models.DecimalField(max_digits=6, decimal_places=3)
    dreb_pct = models.DecimalField(max_digits=6, decimal_places=3)
    reb_pct = models.DecimalField(max_digits=6, decimal_places=3)
    tm_tov_pct = models.DecimalField(max_digits=6, decimal_places=3)
    efg_pct = models.DecimalField(max_digits=6, decimal_places=3)
    ts_pct = models.DecimalField(max_digits=6, decimal_places=3)
    e_pace = models.DecimalField(max_digits=6, decimal_places=3)
    pace = models.DecimalField(max_digits=6, decimal_places=3)
    pace_per40 = models.DecimalField(max_digits=6, decimal_places=3)
    poss = models.PositiveSmallIntegerField()
    pie = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Lineup'
        verbose_name_plural = 'Lineups'
        ordering = ['team_abreviation']


class Player(models.Model):
    player_id = models.CharField(max_length=250, unique=True)
    player_name = models.CharField(max_length=250)
    team_id = models.CharField(max_length=250)
    team_abr = models.CharField(max_length=250)
    age = models.PositiveSmallIntegerField()
    games_played = models.PositiveSmallIntegerField()
    w = models.PositiveSmallIntegerField()
    l = models.PositiveSmallIntegerField()
    w_pct = models.DecimalField(max_digits=6, decimal_places=3)
    min = models.DecimalField(max_digits=6, decimal_places=3)
    e_off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    e_def_rating = models.DecimalField(max_digits=6, decimal_places=3)
    def_rating = models.DecimalField(max_digits=6, decimal_places=3)
    e_net_rating = models.DecimalField(max_digits=6, decimal_places=3)
    net_rating = models.DecimalField(max_digits=6, decimal_places=3)
    ast_pct = models.DecimalField(max_digits=6, decimal_places=3)
    ast_to = models.DecimalField(max_digits=6, decimal_places=3)
    ast_ratio = models.DecimalField(max_digits=6, decimal_places=3)
    oreb_pct = models.DecimalField(max_digits=6, decimal_places=3)
    dreb_pct = models.DecimalField(max_digits=6, decimal_places=3)
    reb_pct = models.DecimalField(max_digits=6, decimal_places=3)
    tm_tov_pct = models.DecimalField(max_digits=6, decimal_places=3)
    e_tov_pct = models.DecimalField(max_digits=6, decimal_places=3)
    efg_pct = models.DecimalField(max_digits=6, decimal_places=3)
    ts_pct = models.DecimalField(max_digits=6, decimal_places=3)
    usg_pct = models.DecimalField(max_digits=6, decimal_places=3)
    e_usg_pct = models.DecimalField(max_digits=6, decimal_places=3)
    e_pace = models.DecimalField(max_digits=6, decimal_places=3)
    pace = models.DecimalField(max_digits=6, decimal_places=3)
    pace_per40 = models.DecimalField(max_digits=6, decimal_places=3)
    pie = models.DecimalField(max_digits=6, decimal_places=3)
    poss = models.PositiveSmallIntegerField()
    fgm = models.PositiveSmallIntegerField()
    fga = models.PositiveSmallIntegerField()
    fgm_pg = models.DecimalField(max_digits=6, decimal_places=1)
    fga_pg = models.DecimalField(max_digits=6, decimal_places=1)
    fg_pct = models.DecimalField(max_digits=6, decimal_places=3)

    def __str__(self):
        return self.player_name

    class Meta:
        verbose_name = 'Player'
        verbose_name_plural = 'Player'
        ordering = ['player_name']


class ShotPrediction(models.Model):
    player = models.CharField(max_length=250)
    home_score = models.PositiveSmallIntegerField()
    away_score = models.PositiveSmallIntegerField()
    time = models.PositiveSmallIntegerField()  # Probar con el duration Field
    is_home = models.BooleanField()
    time_played = models.PositiveSmallIntegerField()  # Probar con el duration Field
    points_scored = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(
        'Created at', default=now, blank=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='shots_predicted', blank=True,
        null=True, editable=False)
    solucion = models.CharField(max_length=250)
    probabilidad = models.CharField(max_length=250)


class LineupStatisticsPrediction(models.Model):
    efg_pct = models.DecimalField(max_digits=6, decimal_places=3)
    ts_pct = models.DecimalField(max_digits=6, decimal_places=3)
    pie = models.DecimalField(max_digits=6, decimal_places=3)
    off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    created_at = models.DateTimeField(
        'Created at', default=now, blank=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='lineup_statistics_predicted', blank=True,
        null=True, editable=False)

    def __str__(self):
        return "EFG%: " + str(self.efg_pct) + " - TS%: " + str(self.ts_pct) + " - PIE:" + str(self.pie)


class LineupPlayersPrediction(models.Model):
    player1 = models.CharField(max_length=250)
    player2 = models.CharField(max_length=250)
    player3 = models.CharField(max_length=250)
    player4 = models.CharField(max_length=250)
    player5 = models.CharField(max_length=250)
    off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    created_at = models.DateTimeField(
        'Created at', default=now, blank=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='lineup_player_predicted', blank=True,
        null=True, editable=False)

    def __str__(self):
        return self.player1 + " - " + self.player2 + " - " + self.player3 + " - " + self.player4 + " - " + self.player5


class LineupsModelRating(models.Model):
    max_off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    min_off_rating = models.DecimalField(max_digits=6, decimal_places=3)
    avg_off_rating = models.DecimalField(max_digits=6, decimal_places=3)

    max_def_rating = models.DecimalField(max_digits=6, decimal_places=3)
    min_def_rating = models.DecimalField(max_digits=6, decimal_places=3)
    avg_def_rating = models.DecimalField(max_digits=6, decimal_places=3)

    max_net_rating = models.DecimalField(max_digits=6, decimal_places=3)
    min_net_rating = models.DecimalField(max_digits=6, decimal_places=3)
    avg_net_rating = models.DecimalField(max_digits=6, decimal_places=3)

    created_at = models.DateTimeField(
        'Created at', default=now, blank=True, editable=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='lineups_model_ratings', blank=True,
        null=True, editable=False)
