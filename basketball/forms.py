from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.password_validation import password_validators_help_texts
from django.core.exceptions import ValidationError

from . import services

User = get_user_model()

CHOICES_TEAMS = [
    ('', '-- Equipo --'),
    ('DEN', 'Denver Nuggets'),
    ('MIN', 'Minnesota Timberwolves'),
    ('OKC', 'Oklahoma City Thunder'),
    ('POR', 'Portland Trail Blazers'),
    ('UTA', 'Utah Jazz'),
    ('DAL', 'Dallas Mavericks'),
    ('HOU', 'Houston Rockets'),
    ('MEM', 'Memphis Grizzlies'),
    ('NOP', 'New Orleans Pelicans'),
    ('SAS', 'San Antonio Spurs'),
    ('GSW', 'Golden State Warriors'),
    ('LAC', 'Los Angeles Clippers'),
    ('LAL', 'Los Angeles Lakers'),
    ('PHX', 'Phoenix Suns'),
    ('SAC', 'Sacramento Kings'),
    ('BOS', 'Boston Celtics'),
    ('BKN', 'Brooklyn Nets'),
    ('NYK', 'New York Knicks'),
    ('PHI', 'Philadelphia 76ers'),
    ('TOR', 'Toronto Raptors'),
    ('CHI', 'Chicago Bulls'),
    ('CLE', 'Cleveland Cavaliers'),
    ('DET', 'Detroit Pistons'),
    ('IND', 'Indiana Pacers'),
    ('MIL', 'Milwaukee Bucks'),
    ('ATL', 'Atlanta Hawks'),
    ('CHA', 'Charlotte Hornets'),
    ('MIA', 'Miami Heat'),
    ('ORL', 'Orlando Magic'),
    ('WAS', 'Washington Wizards')
]

CHOICES_PLAYERS = services.PlayerService().get_all_players_names()


class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': "usuario o email"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': "contraseña"}))

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': "usuario"}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': "email"}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': "contraseña"}), help_text=password_validators_help_texts())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': "confirmación contraseña"}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('El email es necesario')
        elif User.objects.filter(email=email).exists():
            raise ValidationError('El email ya existe')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('El usuario es necesario')
        return username


class ShotPredictorForm(forms.Form):
    player = forms.ChoiceField(required=True, choices=CHOICES_PLAYERS, initial="-- Jugador --",
                               widget=forms.Select(attrs={'class': 'predictplayer'}))

    home_score = forms.IntegerField(label='Marcador Local', min_value=0, required=True,
                                    widget=forms.NumberInput(attrs={'placeholder': 'Marcador Local'}))
    away_score = forms.IntegerField(label='Marcador Visitante', min_value=0, required=True,
                                    widget=forms.NumberInput(attrs={'placeholder': 'Marcador Visitante'}))

    time = forms.IntegerField(label='Tiempo transcurrido', required=True, min_value=0, max_value=80,
                              widget=forms.NumberInput(attrs={'placeholder': 'Tiempo transcurrido (minutos)'}))

    location = forms.ChoiceField(label="Localidad", required=True,
                                 choices=[("", "-- Localidad --"), ("Local", "Local"), ("Visitante", "Visitante")],
                                 initial="-- Localidad --")

    time_played = forms.IntegerField(label='Tiempo jugado', required=True, min_value=0, max_value=80,
                                     widget=forms.NumberInput(attrs={'placeholder': 'Tiempo jugado (minutos)'}))

    points_scored = forms.IntegerField(label='Puntos Anotados', min_value=0, required=True,
                                       widget=forms.NumberInput(attrs={'placeholder': 'Puntos Anotados'}))

    def clean(self):
        time = self.cleaned_data.get('time')
        time_played = self.cleaned_data.get('time_played')
        home_score = self.cleaned_data.get('home_score')
        away_score = self.cleaned_data.get('away_score')
        points_scored = self.cleaned_data.get('points_scored')
        location = self.cleaned_data.get('location')
        if time and time_played and time_played > time:
            raise forms.ValidationError(
                'El tiempo jugado no puede ser mayor que el tiempo transcurrido')

        if (home_score or home_score == 0) and (away_score or away_score == 0) and points_scored and (
                (location == "Local" and points_scored > home_score) or (
                location == "Visitante" and points_scored > away_score)):
            raise forms.ValidationError(
                'La anotación del jugador no puede ser mayor que la anotación de su equipo')
        return self.cleaned_data


class UploadDataForm(forms.Form):
    excel_file = forms.FileField(required=True, widget=forms.FileInput(attrs={'accept': '.csv'}))

    def clean_excel_file(self):
        f = self.cleaned_data['excel_file']
        if f:
            ext = f.name.split('.')[-1]
            if ext != 'csv':
                raise forms.ValidationError('El archivo debe ser de tipo CSV')
        return f


class SearchPlayerFilterForm(forms.Form):
    player_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': "Nombre jugador"}))
    age = forms.IntegerField(required=False, max_value=99, min_value=18, widget=forms.NumberInput(
        attrs={'placeholder': 'Edad', 'min': '18', 'max': '99'}))
    team_abr = forms.ChoiceField(required=False, choices=CHOICES_TEAMS, initial="-- Equipo --")

    def clean_player_name(self):
        player_name = self.cleaned_data.get('player_name')
        player_name_join = player_name.replace(' ', '')
        if player_name and not player_name_join.isalpha():
            raise ValidationError('Introduzca solo letras y espacios')
        return player_name


class SearchLineupFilterForm(forms.Form):
    player_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': "Jugador (Buscar por apellido)"}))
    team_abr = forms.ChoiceField(required=False, choices=CHOICES_TEAMS, initial="-- Equipo --")

    def clean_player_name(self):
        player_name = self.cleaned_data.get('player_name')
        player_name_join = player_name.replace(' ', '')
        if player_name and not player_name_join.isalpha():
            raise ValidationError('Introduzca solo letras y espacios')
        return player_name


class LineupPredictorByPlayersForm(forms.Form):
    player1 = forms.ChoiceField(required=True, choices=CHOICES_PLAYERS, initial="-- Jugador --",
                                widget=forms.Select(attrs={'class': 'predictplayer'}))
    player2 = forms.ChoiceField(required=True, choices=CHOICES_PLAYERS, initial="-- Jugador --",
                                widget=forms.Select(attrs={'class': 'predictplayer'}))
    player3 = forms.ChoiceField(required=True, choices=CHOICES_PLAYERS, initial="-- Jugador --",
                                widget=forms.Select(attrs={'class': 'predictplayer'}))
    player4 = forms.ChoiceField(required=True, choices=CHOICES_PLAYERS, initial="-- Jugador --",
                                widget=forms.Select(attrs={'class': 'predictplayer'}))
    player5 = forms.ChoiceField(required=True, choices=CHOICES_PLAYERS, initial="-- Jugador --",
                                widget=forms.Select(attrs={'class': 'predictplayer'}))

    def clean(self):
        player1 = self.cleaned_data.get('player1')
        player2 = self.cleaned_data.get('player2')
        player3 = self.cleaned_data.get('player3')
        player4 = self.cleaned_data.get('player4')
        player5 = self.cleaned_data.get('player5')

        if player1 == player2 or player1 == player3 or player1 == player4 or player1 == player5 \
                or player2 == player3 or player2 == player4 or player2 == player5 \
                or player3 == player4 or player3 == player5 \
                or player4 == player5:
            raise forms.ValidationError(
                'No puedes seleccionar dos veces al mismo jugador')
        return self.cleaned_data


class LineupPredictorByStatisticsForm(forms.Form):
    efg_pct = forms.DecimalField(min_value=0, max_value=100, decimal_places=2, required=True,
                                 widget=forms.NumberInput(
                                     attrs={'placeholder': 'Effective Field Goal Percentage:  Ej (55.55)'}))
    ts_pct = forms.DecimalField(min_value=0, max_value=100, decimal_places=2, required=True,
                                widget=forms.NumberInput(
                                    attrs={'placeholder': 'True Shooting Percentage:  Ej (55.55)'}))
    pie = forms.DecimalField(min_value=0, max_value=100, decimal_places=2, required=True,
                             widget=forms.NumberInput(attrs={'placeholder': 'Player Impact Estimate:  Ej (55.55)'}))
