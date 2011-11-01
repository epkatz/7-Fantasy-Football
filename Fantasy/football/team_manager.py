from Fantasy.football.models import Trade
from models import Player, Team

STARTING_BUDGET = 100
MAX_PLAYERS = 15

def drop_player(player):
    if player is None or player.team is None:
        return False
    if player.team.size == 0:
        return False
    if not player.benched:
        bench(player)
    team = player.team
    team.size = team.size - 1
    team.budget = team.budget + player.salary
    player.team = None
    team.save()
    player.save()
    return True

def add_player(player, team):
    if player is None or team is None:
        return False
    if not player.is_free_agent():
        return False
    if team.size == MAX_PLAYERS:
        return False
    if team.budget - player.salary < 0:
        return False
    player.team = team
    player.benched = True
    team.size = team.size + 1
    team.budget = team.budget - player.salary
    player.save()
    team.save()
    return True

#Take a player off the bench
def play(player, position):
    if player is None or player.team is None:
        return False
    if not player.benched:
        return False
    if player.position != position:
        return False
    team = player.team
    if player.position == "QB" and team.qb_count == 0:
        team.qb_count = team.qb_count + 1
    elif player.position == "RB" and team.rb_count < 2:
        team.rb_count = team.rb_count + 1
    elif player.position == "WR" and team.wr_count < 2:
        team.wr_count = team.wr_count + 1
    elif player.position == "PK" and team.pk_count == 0:
        team.pk_count = team.pk_count + 1
    elif player.position == "ST" and team.st_count == 0:
        team.st_count = team.st_count + 1
    elif player.position == "TE" and team.te_count == 0:
        team.te_count = team.te_count + 1
    else:
        return False
    player.benched=False
    team.save()  
    player.save()
    return True
        
#Bench a player
def bench(player):
    if player is None or player.team is None:
        return False
    if player.benched:
        return False
    team = player.team
    if player.position == "QB" and team.qb_count == 1:
        team.qb_count = 0
    elif player.position == "RB" and team.rb_count > 0:
        team.rb_count = team.rb_count - 1
    elif player.position == "WR" and team.wr_count > 0:
        team.wr_count = team.wr_count - 1
    elif player.position == "PK" and team.pk_count == 1:
        team.pk_count = 0
    elif player.position == "ST" and team.st_count == 1:
        team.st_count = 0
    elif player.position == "TE" and team.te_count == 1:
        team.te_count = 0
    else:
        return False
    player.benched=True
    team.save()
    player.save() 
    return True

#Given an active player and a player on the bench, swap them
def swap_players(player1, player2):
    if player1 is None or player2 is None:
        return False
    if player1.benched or not player2.benched:
        return False
    if player1.position != player2.position:
        return False
    if not on_same_team(player1, player2):
        return False
    player1.benched = True
    player2.benched = False
    player1.save()
    player2.save()
    return True

#Request a trade by adding the trade to the Trades table
def request_trade(players1, team1, players2, team2):
    if players1 is None or team1 is None or players2 is None or team2 is None:
        return 'Bad Trade Values'
    if len(players1) == 0 or len(players2) == 0:
        return 'Each team must offer at least one player'
    if not all_on_same_team(players1,team1) or not all_on_same_team(players2,team2):
        return 'Can only trade your own players'
    if check_size_and_salary(players1,team1,players2,team2) is None:
        return 'The trade must fall within your budget and team size'
    trades = Trade.objects.values('tid').order_by('-tid').distinct()[:1]
    trade_id = 0
    if len(trades) > 0:
        trade_id = int(trades[0]['tid']) + 1
    for player1 in players1:
        trade = Trade(tid=trade_id,team_from=team1,team_to=team2,player=player1, proposed_trade=team1, to_approve=team2)
        trade.save()
    for player2 in players2:
        trade = Trade(tid=trade_id,team_from=team2,team_to=team1,player=player2, proposed_trade=team1, to_approve=team2)
        trade.save()
    trade_id = trade_id + 1
    return 'Trade Requested'

#Verify the new sizes and salaries are not problematic
def check_size_and_salary(players1,team1,players2,team2):
    new_size1 = team1.size - len(players1) + len(players2)
    new_size2 = team2.size - len(players2) + len(players1)
    new_budget1 = team1.budget
    new_budget2 = team2.budget
    for player1 in players1:
        new_budget1 = new_budget1 - player1.salary
        new_budget2 = new_budget2 + player1.salary
    for player2 in players2:
        new_budget1 = new_budget1 + player2.salary
        new_budget2 = new_budget2 - player2.salary
    if new_size1 > MAX_PLAYERS or new_size1 < 0:
        return None
    if new_size2 > MAX_PLAYERS or new_size2 < 0:
        return None
    if new_budget1 > STARTING_BUDGET or new_budget1 < 0:
        return None
    if new_budget2 > STARTING_BUDGET or new_budget2 < 0:
        return None
    dict = {'size1': new_size1, 'size2': new_size2, 'budget1': new_budget1, 'budget2': new_budget2}
    return dict

#Trade two lists or players
def confirm_trade(tid):
    trades = Trade.objects.filter(tid__exact = tid)
    #Get the two teams and verify there are only two
    players1 = []
    players2 = []
    team1 = None
    team2 = None
    for trade in trades:
        if team1 is None:
            team1 = trade.team_to
        if team2 is None:
            team2 = trade.team_from
        if same_team(trade.player.team, team1):
            players1.append(trade.player)
        elif same_team(trade.player.team, team2):
            players2.append(trade.player)
        else:
            #There are more than two teams in this trade
            delete_trade(tid)
            return False
    #Verify the new sizes are not problematic
    info = check_size_and_salary(players1,team1,players2,team2)
    if info is None:
        return False
    #Swap teams
    for player1 in players1:
        print "adding " + player1.full_name + " to " + team2.team_name + "\n"
        player1.team = team2
        player1.benched = True
        player1.save()
    for player2 in players2:
        print "adding " + player2.full_name + " to " + team1.team_name + "\n"
        player2.team = team1
        player2.benched = True
        player2.save()
    team1.size = info['size1']
    team1.budget = info['budget1']
    team1.save()
    team2.size = info['size2']
    team2.budget = info['budget2']
    team2.save()
    delete_trade(tid)
    return True

def delete_trade(tid):
    trades = Trade.objects.filter(tid__exact=tid)
    for trade in trades:
        trade.delete()

#Returns a list of all the tids for a given team
def get_trades(team):
    return Trade.objects.filter(team = team).distinct('tid')

#Verify that all players belong to a single team
#(free agent does not count as a team)
def all_on_same_team(players, team):
    for player in players:
        if player is None:
            return False
        if player.is_free_agent():
            return False
        if not same_team(team, player.team):
            return False;
    return True

#Verify that two teams are the same (free agent is considered a team)
def same_team(team1, team2):
    if team1 is None and team2 is None:
        return True
    if team1 is None or team2 is None:
        return False
    return team1.pk == team2.pk

#Verify that two players are on the same team (free agent is considered a team)
def on_same_team(player1, player2):
    if player1 == None or player2 == None:
        return False
    return same_team(player1.team,player2.team)
