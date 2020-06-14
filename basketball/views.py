import csv
import io
import re

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.handlers import exception
from django.core.paginator import InvalidPage
from django.db import transaction
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
import pandas as pd
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic
from joblib import load
from sklearn.preprocessing import PolynomialFeatures

# Create your views here.
from . import forms, services, models
from .models import Player, Lineup, ShotPrediction
from .services import PlayerService, LineupService


def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'home.html', context)


class SignUpView(generic.CreateView):
    form_class = forms.RegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        user = form.save()
        services.ProfileService().create(user)
        login(self.request, user, backend=settings.AUTHENTICATION_BACKENDS[1])
        return super(SignUpView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class LineupPredictorByStatisticsFormView(generic.FormView):
    form_class = forms.LineupPredictorByStatisticsForm
    template_name = 'lineupPrediction/lineup_predictor_by_statistics.html'
    success_url = '/lineup/predictorByStatistics'

    def form_valid(self, form):
        efg_pct = float(self.request.POST.get('efg_pct')) / 100
        ts_pct = float(self.request.POST.get('ts_pct')) / 100
        pie = float(self.request.POST.get('pie')) / 100

        model_reload = load('./modelosquintetos/predictorQuintetosEstadisticas.joblib')

        x_pred = pd.DataFrame(columns=('EFG', 'TS', 'PIE'))  # Creo dataframe vacío
        x_pred.loc[len(x_pred)] = [efg_pct, ts_pct, pie]

        # Definimos el grado del polinomio
        poli_reg = PolynomialFeatures(degree=3)

        # Transformamos en caracteristicas de mayor grado
        x_pred_poli = poli_reg.fit_transform(x_pred)

        solucion = model_reload.predict(x_pred_poli)

        context = self.get_context_data()
        context['solucion'] = solucion

        services.LineupPredictionByStatisticsService().create(efg_pct, ts_pct, pie, solucion, self.request.user)
        context['historico'] = services.LineupsModelRatingService().get_last()
        return render(self.request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class LineupPredictorByPlayersFormView(generic.FormView):
    form_class = forms.LineupPredictorByPlayersForm
    template_name = 'lineupPrediction/lineup_predictor_by_players.html'
    success_url = '/lineup/predictorByPlayers'

    def form_valid(self, form):
        player1 = self.request.POST.get('player1')
        player2 = self.request.POST.get('player2')
        player3 = self.request.POST.get('player3')
        player4 = self.request.POST.get('player4')
        player5 = self.request.POST.get('player5')

        model_reload = load('./modelosquintetos/predictorQuintetosJugadores.joblib')

        x_pred = services.LineupPredictionByPlayersService().statistics_5_players(player1, player2, player3, player4,
                                                                                  player5)
        solucion = model_reload.predict(x_pred)

        context = self.get_context_data()
        context['solucion'] = solucion

        services.LineupPredictionByPlayersService().create(player1, player2, player3, player4, player5, solucion,
                                                           self.request.user)
        context['historico'] = services.LineupsModelRatingService().get_last()
        return render(self.request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ShotPredictorFormView(generic.FormView):
    form_class = forms.ShotPredictorForm
    template_name = 'shotPrediction/shot_predictor.html'
    success_url = '/shot/predictor'

    def form_valid(self, form):

        player = self.request.POST.get('player')
        try:
            model_reload = load('./modelostiro/player-joblib-' + player + '.joblib')
        except Exception as e:
            context = self.get_context_data()
            context['noPlayer'] = 'Este jugador no ha jugado o no se ha podido encontrar a dicho jugador'
            return render(self.request, self.template_name, context)

        home_score = self.request.POST.get('home_score')
        away_score = self.request.POST.get('away_score')
        time = self.request.POST.get('time')

        if self.request.POST.get('location') == "Local":
            is_home = 1
        elif self.request.POST.get('location') == "Visitante":
            is_home = 0

        time_played = self.request.POST.get('time_played')
        points_scored = self.request.POST.get('points_scored')

        x_pred = pd.DataFrame(columns=(
            'HOME_SCORE', 'AWAY_SCORE', 'TIME', 'TOTAL_POINTS_SCORED', 'IS_HOME',
            'TIME_PLAYED'))  # Creo dataframe vacío
        x_pred.loc[len(x_pred)] = [home_score, away_score, time, points_scored, is_home, time_played]

        solucion = model_reload.predict(x_pred)
        probabilidad = model_reload.predict_proba(x_pred)


        context = self.get_context_data()
        context['probabilidad'] = ''
        if solucion == 1:  # 1 entra
            context['solucion'] = 'será anotado'
            context['probabilidad'] = float(probabilidad[0][0]) * 100
        else:  # 2 falla
            context['solucion'] = 'será fallado'
            context['probabilidad'] = float(probabilidad[0][1]) * 100

        services.ShotPredictionService().create(player, home_score, away_score, time, is_home, time_played,
                                                points_scored, self.request.user, context['solucion'],
                                                context['probabilidad'])
        return render(self.request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class UploadPlayerDataFormView(generic.FormView):
    form_class = forms.UploadDataForm
    template_name = 'player/upload_player_data.html'
    success_url = '/admin/basketball/player/'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.render_to_response(self.get_context_data())
        else:
            return HttpResponseRedirect("/home")

    def form_valid(self, form):
        try:
            f = io.TextIOWrapper(form.cleaned_data.get('excel_file').file)
            reader = csv.DictReader(f)
            with transaction.atomic():
                for player in reader:
                    services.PlayerService().create_and_save_player_from_csv(player)
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            return render(self.request, 'error.html', context={'exception': e, 'data': 'player'})


@method_decorator(login_required, name='dispatch')
class UploadLineupDataFormView(generic.FormView):
    form_class = forms.UploadDataForm
    template_name = 'lineup/upload_lineup_data.html'
    success_url = '/admin/basketball/lineup/'

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return self.render_to_response(self.get_context_data())
        else:
            return HttpResponseRedirect("/home")

    def form_valid(self, form):
        try:
            f = io.TextIOWrapper(form.cleaned_data.get('excel_file').file)
            reader = csv.DictReader(f)
            with transaction.atomic():
                for lineup in reader:
                    services.LineupService().create_and_save_lineup_from_csv(lineup)
            services.LineupsModelRatingService().create_statistics(self.request.user)
            return HttpResponseRedirect(self.get_success_url())
        except Exception as e:
            return render(self.request, 'error.html', context={'exception': e, 'data': 'lineup'})


def delete_all_players_view(request):
    if request.user.is_superuser:
        services.PlayerService().delete_all_players()
        return HttpResponseRedirect("/admin/basketball/player/")
    else:
        return HttpResponseRedirect("/home")


def delete_all_lineups_view(request):
    if request.user.is_superuser:
        services.LineupService().delete_all_lineups()
        return HttpResponseRedirect("/admin/basketball/lineup/")
    else:
        return HttpResponseRedirect("/home")


@method_decorator(login_required, name='dispatch')
class PlayerFilterFormView(generic.FormView):
    form_class = forms.SearchPlayerFilterForm
    template_name = 'player/list_search_player.html'

    def form_valid(self, form):
        data = form.cleaned_data
        kwargs = {}
        kwargs['player_name'] = data.pop('player_name', None) or None
        kwargs['age'] = data.pop('age', None) or None
        kwargs['team_abr'] = data.pop('team_abr', None) or None

        self.request.session['form_values'] = self.request.POST

        kwargs = {key: val for key, val in kwargs.items() if val}

        return redirect(reverse('list_player_filter', kwargs=kwargs))

    def form_invalid(self, form):
        self.request.session['form_values'] = self.request.POST
        return redirect('list_player_filter')


@method_decorator(login_required, name='dispatch')
class PlayerFilterListView(generic.ListView):
    model = Player
    template_name = 'player/list_search_player.html'
    paginate_by = 12
    form_class = forms.SearchPlayerFilterForm

    def get_context_data(self, **kwargs):
        context = super(PlayerFilterListView,
                        self).get_context_data(**kwargs)
        context['form'] = self.form_class(
            self.request.session.get('form_values'))

        return context

    def get_queryset(self):
        self.kwargs['player_name__icontains'] = self.kwargs.pop(
            'player_name', None) or None
        self.kwargs['age__exact'] = self.kwargs.pop(
            'age', None) or None
        self.kwargs['team_abr__exact'] = self.kwargs.pop(
            'team_abr', None) or None

        queryset = services.PlayerService().players_filter_search(**self.kwargs)

        return queryset


@method_decorator(login_required, name='dispatch')
class LineupFilterFormView(generic.FormView):
    form_class = forms.SearchLineupFilterForm
    template_name = 'lineup/list_search_lineup.html'

    def form_valid(self, form):
        data = form.cleaned_data
        kwargs = {}
        kwargs['player_name'] = data.pop('player_name', None) or None
        kwargs['team_abr'] = data.pop('team_abr', None) or None

        self.request.session['form_values'] = self.request.POST

        kwargs = {key: val for key, val in kwargs.items() if val}

        return redirect(reverse('list_lineup_filter', kwargs=kwargs))

    def form_invalid(self, form):
        self.request.session['form_values'] = self.request.POST
        return redirect('list_lineup_filter')


@method_decorator(login_required, name='dispatch')
class LineupFilterListView(generic.ListView):
    model = Lineup
    template_name = 'lineup/list_search_lineup.html'
    paginate_by = 12
    form_class = forms.SearchLineupFilterForm

    def get_context_data(self, **kwargs):
        context = super(LineupFilterListView,
                        self).get_context_data(**kwargs)
        context['form'] = self.form_class(
            self.request.session.get('form_values'))

        return context

    def get_queryset(self):
        self.kwargs['group_name__icontains'] = self.kwargs.pop(
            'player_name', None) or None
        self.kwargs['team_abreviation__exact'] = self.kwargs.pop(
            'team_abr', None) or None
        queryset = services.LineupService().lineups_filter_search(**self.kwargs)

        return queryset


@method_decorator(login_required, name='dispatch')
class ShotPredictionsListView(generic.ListView):
    model = ShotPrediction
    template_name = 'shotPrediction/list_shot_prediction.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = services.ShotPredictionService().my_predictions(self.request.user).order_by('-created_at')
        return queryset


@method_decorator(login_required, name='dispatch')
class LineupPredictionsListView(generic.ListView):
    template_name = 'lineupPrediction/list_lineup_prediction.html'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super(LineupPredictionsListView, self).get_context_data(*args, **kwargs)

        queryset2 = services.LineupPredictionByStatisticsService().my_predictions(
            self.request.user).order_by('-created_at')
        page_size2 = self.get_paginate_by(queryset2)
        context_object_name2 = self.get_context_object_name(queryset2)

        if page_size2:
            paginator2, page2, queryset2, is_paginated2 = self.paginate_queryset2(queryset2, page_size2)

            context['paginator2'] = paginator2
            context['page_obj2'] = page2
            context['is_paginated2'] = is_paginated2
            context['object_list2'] = queryset2
        else:

            context['paginator2'] = None
            context['page_obj2'] = None
            context['is_paginated2'] = None
            context['object_list2'] = queryset2

        if context_object_name2 is not None:
            context[context_object_name2] = queryset2

        context['ten_off_ratings'] = services.LineupPredictionByPlayersService().my_last_predictions(self.request.user)
        context['ten_off_ratings_statistics'] = services.LineupPredictionByStatisticsService().my_last_predictions(self.request.user)


        return context

    def get_queryset(self):
        queryset = services.LineupPredictionByPlayersService().my_predictions(self.request.user).order_by('-created_at')
        return queryset

    def paginate_queryset2(self, queryset, page_size):
        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty())
        page = self.request.GET.get('page2') or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_('Page is not “last”, nor can it be converted to an int.'))
        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_('Invalid page (%(page_number)s): %(message)s') % {
                'page_number': page_number,
                'message': str(e)
            })


@method_decorator(login_required, name='dispatch')
class PlayerDetailView(generic.DetailView):
    model = Player
    template_name = 'player/player_detail.html'

    def get_context_data(self, **kwargs):
        player = kwargs.get('object')
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        team_players = services.PlayerService().find_players_by_team_id(player.team_id)
        context['team_players'] = team_players
        return context


@method_decorator(login_required, name='dispatch')
class LineupDetailView(generic.DetailView):
    model = Lineup
    template_name = 'lineup/lineup_detail.html'

    def get_context_data(self, **kwargs):
        lineup = kwargs.get('object')
        context = super(LineupDetailView, self).get_context_data(**kwargs)
        grupo_id = re.match("-(.*)-(.*)-(.*)-(.*)-(.*)-", lineup.group_id)
        context["player1"] = services.PlayerService().find_player_by_id(grupo_id.group(1))
        context["player2"] = services.PlayerService().find_player_by_id(grupo_id.group(2))
        context["player3"] = services.PlayerService().find_player_by_id(grupo_id.group(3))
        context["player4"] = services.PlayerService().find_player_by_id(grupo_id.group(4))
        context["player5"] = services.PlayerService().find_player_by_id(grupo_id.group(5))
        return context
