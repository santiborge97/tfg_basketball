from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('auth/signup/', views.SignUpView.as_view(), name='signup'),
    path('shot/predictor', views.ShotPredictorFormView.as_view(), name='shot_predictor'),
    path('uploadPlayerData', views.UploadPlayerDataFormView.as_view(), name='upload_player_data'),
    path('uploadLineupData', views.UploadLineupDataFormView.as_view(), name='upload_lineup_data'),
    path('deletePlayer', views.delete_all_players_view, name='delete_all_players'),
    path('deleteLineup', views.delete_all_lineups_view, name='delete_all_lineups'),
    path('player/filter', views.PlayerFilterFormView.as_view(), name='player_filter'),
    re_path(r'^players/(?:(?P<team_abr>[A-Z]{3})/)?(?:(?P<player_name>[a-zA-Z\u00C0-\u00FF\s]*)/)?(?:(?P<age>\d{2})/)?$',
            views.PlayerFilterListView.as_view(), name='list_player_filter'),
    path('lineups/filter', views.LineupFilterFormView.as_view(), name='lineup_filter'),
    re_path(r'^lineups/(?:(?P<team_abr>[A-Z]{3})/)?(?:(?P<player_name>[a-zA-Z\u00C0-\u00FF\s]*)/)?$',
            views.LineupFilterListView.as_view(), name='list_lineup_filter'),
    path('shot/predictor/list', views.ShotPredictionsListView.as_view(), name='shot_predictions_list'),
    path('lineup/predictor/list', views.LineupPredictionsListView.as_view(), name='lineup_predictions_list'),
    path('player/<int:pk>', views.PlayerDetailView.as_view(), name='detail_player'),
    path('lineup/<int:pk>', views.LineupDetailView.as_view(), name='detail_lineup'),
    path('lineup/predictorByStatistics', views.LineupPredictorByStatisticsFormView.as_view(), name='lineup_predictor_by_statistics'),
    path('lineup/predictorByPlayers', views.LineupPredictorByPlayersFormView.as_view(), name='lineup_predictor_by_players'),

]
