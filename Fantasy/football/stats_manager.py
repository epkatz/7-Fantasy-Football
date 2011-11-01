from models import Player, Team
import random

def generate_stats():
    for player in Player.objects.all():
        stat = int(random.randint(1,40) / (16 - player.salary))
        team = player.team
        if player.week1 == 0:
            player.week1 = stat
            player.total_pts = stat
            player.average_pts = stat
            if not player.is_free_agent() and not player.benched:
                team.week1 = team.week1 + stat
        elif player.week2 == 0:
            player.week2 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (player.average_pts + stat) / 2
            if not player.is_free_agent() and not player.benched:
                team.week2 = team.week2 + stat
        elif player.week3 == 0:
            player.week3 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (2*player.average_pts + stat) / 3
            if not player.is_free_agent() and not player.benched:
                team.week3 = team.week3 + stat
        elif player.week4 == 0:
            player.week4 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (3*player.average_pts + stat) / 4
            if not player.is_free_agent() and not player.benched:
                team.week4 = team.week4 + stat
        elif player.week5 == 0:
            player.week5 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (4*player.average_pts + stat) / 5
            if not player.is_free_agent() and not player.benched:
                team.week5 = team.week5 + stat
        elif player.week6 == 0:
            player.week6 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (5*player.average_pts + stat) / 6
            if not player.is_free_agent() and not player.benched:
                team.week6 = team.week6 + stat
        elif player.week7 == 0:
            player.week7 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (6*player.average_pts + stat) / 7
            if not player.is_free_agent() and not player.benched:
                team.week7 = team.week7 + stat
        elif player.week8 == 0:
            player.week8 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (7*player.average_pts + stat) / 8
            if not player.is_free_agent() and not player.benched:
                team.week8 = team.week8 + stat
        elif player.week9 == 0:
            player.week9 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (8*player.average_pts + stat) / 9
            if not player.is_free_agent() and not player.benched:
                team.week9 = team.week9 + stat
        elif player.week10 == 0:
            player.week10 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (9*player.average_pts + stat) / 10
            if not player.is_free_agent() and not player.benched:
                team.week10 = team.week10 + stat
        elif player.week11 == 0:
            player.week11 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (10*player.average_pts + stat) / 11
            if not player.is_free_agent() and not player.benched:
                team.week11 = team.week11 + stat
        elif player.week12 == 0:
            player.week12 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (11*player.average_pts + stat) / 12
            if not player.is_free_agent() and not player.benched:
                team.week12 = team.week12 + stat
        elif player.week13 == 0:
            player.week13 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (12*player.average_pts + stat) / 13
            if not player.is_free_agent() and not player.benched:
                team.week13 = team.week13 + stat
        elif player.week14 == 0:
            player.week14 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (13*player.average_pts + stat) / 14
            if not player.is_free_agent() and not player.benched:
                team.week14 = team.week14 + stat
        elif player.week15 == 0:
            player.week15 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (14*player.average_pts + stat) / 15
            if not player.is_free_agent() and not player.benched:
                team.week15 = team.week15 + stat
        elif player.week16 == 0:
            player.week16 = stat
            player.total_pts = player.total_pts + stat
            player.average_pts = (15*player.average_pts + stat) / 16
            if not player.is_free_agent() and not player.benched:
                team.week16 = team.week16 + stat
        else:
            return False
        player.save()
        if not player.is_free_agent() and not player.benched:
            team.total_pts = team.total_pts + stat
            team.save()
    update_ranks()
    return True

def update_ranks():
    teams = Team.objects.all().order_by('-total_pts')
    i = 1
    for team in teams:
        team.current_rank = i
        i = i + 1
        team.save()
