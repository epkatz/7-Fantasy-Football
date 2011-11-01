from Fantasy.football.models import Team, Player, Trade
from Fantasy.football.myteam_views import raw_myteam
from Fantasy.football.stats_manager import generate_stats
from Fantasy.football.team_manager import request_trade, confirm_trade
from collections import defaultdict
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response, redirect
from django.utils.encoding import smart_str
from httplib import HTTPResponse
    
    
@login_required
def accept_trade(request):
    if request.method == 'POST':
        tid = request.POST['tid']
        success = confirm_trade(tid)
        if success:
            return raw_myteam(request, 'Trade Succesful')
        else:
            return raw_myteam(request, 'Unable to Complete Trade ' + tid)
    return redirect('/pending_trades')

@login_required
def pending_trades(request):
    my_team = Team.objects.get(owner=request.user)
    my_trades = Trade.objects.filter(to_approve=my_team).order_by('tid')
    trade_dict = defaultdict(list)
    for trade in my_trades:
        trade_message = trade.team_from.team_name + ' trades ' + trade.player.full_name + ' to ' + trade.team_to.team_name
        trade_message = smart_str(trade_message, encoding='utf-8', strings_only=False, errors='strict')
        trade_dict[str(trade.tid)].append(trade_message)
    print trade_dict.items()
    return render_to_response('index.html', {'template_name' : 'pending_trades.html', 'trades' : trade_dict.items()})

@login_required
def make_trade(request):
    if request.method == 'POST':
        team1 = Team.objects.get(pk=request.POST['team1_pk'])
        team2 = Team.objects.get(pk=request.POST['team2_pk'])
        team1_players_pk = request.POST.getlist('players_team1')
        team2_players_pk = request.POST.getlist('players_team2')
        players1 = []
        players2 = []
        for player_pk in team1_players_pk:
            players1.append(Player.objects.get(pk=player_pk))   
        for player_pk in team2_players_pk:
            players2.append(Player.objects.get(pk=player_pk))
        error_message = request_trade(players1, team1, players2, team2)
        return raw_trade_with(request, team1, team2, error_message) 
    return raw_trade_with(request, team1, team2, 'Could Not Execute Trade')

@login_required
def trade_with(request):
    if request.method == 'POST':
        team1 = Team.objects.get(owner=request.user)
        team2 = Team.objects.get(pk=request.POST['team_pk'])
        return raw_trade_with(request, team1, team2, None)
    return redirect('/trade')

def raw_trade_with(request, team1, team2, error_message):
        players1 = Player.objects.filter(team=team1)
        players2 = Player.objects.filter(team=team2)
        return render_to_response('index.html',   \
                                  {'template_name' : 'trade_with.html', 'team1' : team1, 'team2' : \
                                   team2, 'players1' : players1, 'players2' : players2, 'error_message' : error_message})
        
@login_required
@permission_required('football.add_week', login_url='/')
def add_week(request):
    week = get_week()
    if week is None:
        return render_to_response('index.html', {'template_name' : 'error.html', 'error_message' : 'Season is over'})
    return render_to_response('index.html', {'template_name' : 'add_week.html', 'week' : week})

@login_required
@permission_required('football.add_week', login_url='/')
def add_stats(request):
    generate_stats()
    return redirect('/scoreboard/')
    

def get_week():
    players = Player.objects.all()
    week = None
    if players[0].week16 == 0:
        week = ' - Week 16'
    if players[0].week15 == 0:
        week = ' - Week 15'
    if players[0].week14 == 0:
        week = ' - Week 14'
    if players[0].week13 == 0:
        week = ' - Week 13'
    if players[0].week12 == 0:
        week = ' - Week 12'
    if players[0].week11 == 0:
        week = ' - Week 11'
    if players[0].week10 == 0:
        week = ' - Week 10'
    if players[0].week9 == 0:
        week = ' - Week 9'
    if players[0].week8 == 0:
        week = ' - Week 8'
    if players[0].week7 == 0:
        week = ' - Week 7'
    if players[0].week6 == 0:
        week = ' - Week 6'
    if players[0].week5 == 0:
        week = ' - Week 5'
    if players[0].week4 == 0:
        week = ' - Week 4'
    if players[0].week3 == 0:
        week = ' - Week 3'
    if players[0].week2 == 0:
        week = ' - Week 2'
    if players[0].week1 == 0:
        week = ' - Week 1' 
    return week


@login_required
def scoreboard(request):
    teams = Team.objects.all().order_by('current_rank')
    if (len(teams) == 0):
        return render_to_response('index.html', {'template_name' : 'error.html', 'error_message' : 'No Teams Dumbass'})
    week = get_week()
    if week is None:
        week = " - Final Standings"
    return render_to_response('index.html', {'template_name' : 'scoreboard.html', 'teams' : teams, 'week' : week})

@login_required
def pick_counterpart(request):
    myteam = Team.objects.get(owner=request.user)
    teams = Team.objects.filter(~Q(team_name=myteam.team_name))
    return render_to_response('index.html', {'template_name' : 'counterpart_teams.html', 'teams' : teams})

    
    
    