from Fantasy.football.models import Team, Player
from Fantasy.football.team_manager import bench, play, add_player, drop_player
from Fantasy.football.views import add_message_all
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response, redirect

@login_required
def add_from_free_agent(request):
    player_pk = request.POST['player_pk']
    player = Player.objects.get(pk=player_pk)
    team = Team.objects.get(owner=request.user)
    success = add_player(player, team)
    if success:
        add_message_all(request.user.username + ' added ' + player.full_name)
        return raw_show_free_agents(request, 'Added ' + player.full_name)
    else:
        return raw_show_free_agents(request, 'Could not add player')

@login_required
def show_free_agents(request):
    error_message = None
    return raw_show_free_agents(request, error_message)

def raw_show_free_agents(request, error_message):
    players_list = Player.objects.filter(team=None).order_by('full_name')
    paginator = Paginator(players_list, 20)
    page = request.GET.get('page')
    if page is not None:
        try:
            players = paginator.page(page)
        except PageNotAnInteger:
            players = paginator.page(1)
        except EmptyPage:
            players = paginator.page(paginator.num_pages)
    else:
        players = paginator.page(1)
    if error_message is None:
        return render_to_response('index.html', {'template_name' : 'free_agents.html', 'players' : players})
    else:
        return render_to_response('index.html', {'template_name' : 'free_agents.html', 'players' : players, 'error_message' : error_message})

@login_required
def myteam(request):
    error_message = None
    return raw_myteam(request, error_message)

@login_required
def do_drop_player(request):
    player_pk = request.POST['player_pk']
    player = Player.objects.get(pk=player_pk)
    success = drop_player(player)
    if success:
        add_message_all(request.user.username + ' dropped ' + player.full_name)
        error_message = "Dropped " + player.full_name
        return raw_myteam(request, error_message)
    else:
        error_message = "Cannot Drop " + player.full_name
        return raw_myteam(request, error_message)

def raw_myteam(request, error_message):  
    me = request.user
    my_team = Team.objects.get(owner=me)
    my_players = Player.objects.filter(team=my_team).order_by('position')
    if error_message is None:
        return render_to_response('index.html', {'template_name' : 'myteam.html', 'players' : my_players, 'team' : my_team})
    else:
        return render_to_response('index.html', {'template_name' : 'myteam.html', 'players' : my_players, 'error_message' : error_message, 'team' : my_team})

@login_required
def bench_player(request):
    if request.method == 'POST':
        player_pk = request.POST['player_pk']
        player = Player.objects.get(pk=player_pk)
        bench(player)
        return redirect('/myteam/')
    return render_to_response('index.html', {'template_name' : 'error.html', 'error_message' : 'Could not move to bench'})

@login_required
def start_player(request):
    if request.method == 'POST':
        player_pk = request.POST['player_pk']
        player_position = request.POST['player_position']
        player = Player.objects.get(pk=player_pk)
        success = play(player, player_position)
        if success:
            return redirect('/myteam/')
        else:
            return raw_myteam(request, 'Could not move ' + player.full_name + ' to ' + player_position)
    return render_to_response('index.html', {'template_name' : 'error.html', 'error_message' : 'Could not move to starter'})