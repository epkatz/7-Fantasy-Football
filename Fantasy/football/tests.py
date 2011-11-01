"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Player, Team
from django.contrib.auth.models import User
from team_manager import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_swap_players_valid(self):
        User.objects.create_user("dillen", "der2127@columbia.edu", "letmein")
        User.objects.create_user("eli", "epk2102@columbia.edu", "letmein")
        
        team1 = Team(team_name="Winners",owner=User.objects.get(username__exact="dillen"))
        team2 = Team(team_name="Losers",owner=User.objects.get(username__exact="eli"))
        team1.save()
        team2.save()

        p1 = Player(full_name="abc1",position="WR",team=team1,benched=False)
        p1_rb = Player(full_name="abc2",position="RB",team=team1,benched=False)
        p1_benched = Player(full_name="abc3",position="WR",team=team1)
        p1_team2 = Player(full_name="abc4",position="WR",team=team2,benched=False)
        p1.save()
        p1_rb.save()
        p1_benched.save()
        p1_team2.save()
        
        p2 = Player(full_name="def1",position="WR",team=team1)
        p2_rb = Player(full_name="def2",position="RB",team=team1)
        p2_not_benched = Player(full_name="def3",position="WR",benched=False,team=team1)
        p2_team2 = Player(full_name="def4",position="WR",team=team2)
        p2.save()
        p2_rb.save()
        p2_not_benched.save()
        p2_team2.save()
        
        #Swap p1 and p2
        self.assertEqual(swap_players(p1,p2),True)
        self.assertEqual(p1.benched,True)
        self.assertEqual(p2.benched,False)
        self.assertEqual(swap_players(p2,p1),True)
        self.assertEqual(p1.benched,False)
        self.assertEqual(p2.benched,True)
        
        #Try to swap a wr and rb
        self.assertEqual(swap_players(p1,p2_rb),False)
        self.assertEqual(p1.benched,False)
        self.assertEqual(p2_rb.benched,True)
        
        #Try to swap two not benched wr's
        self.assertEqual(swap_players(p1,p2_not_benched),False)
        self.assertEqual(p1.benched,False)
        self.assertEqual(p2_not_benched.benched,False)
        
        #Try to swap a benched wr with a not benched wr
        self.assertEqual(swap_players(p1_benched,p2),False)
        self.assertEqual(p1_benched.benched,True)
        self.assertEqual(p2.benched,True)
        
        #Try to swap two players from different teams
        self.assertEqual(swap_players(p1_team2,p2),False)
        self.assertEqual(p1_team2.benched,False)
        self.assertEqual(p2.benched,True)
        self.assertEqual(swap_players(p1,p2_team2),False)
        self.assertEqual(p1.benched,False)
        self.assertEqual(p2_team2.benched,True)

    def test_play(self):
        User.objects.create_user("dillen", "der2127@columbia.edu", "letmein")
        User.objects.create_user("eli", "epk2102@columbia.edu", "letmein")
        
        team1 = Team(team_name="Winners",owner=User.objects.get(username__exact="dillen"))

        p1 = Player(full_name="abc1",position="WR",team=team1,benched=False)
        team1.wr_count = 1
        p2 = Player(full_name="abc2",position="WR",team=team1)
        p3 = Player(full_name="abc3",position="WR")
        p4 = Player(full_name="abc4",position="QB",team=team1,benched=False)
        team1.qb_count = 1
        p5 = Player(full_name="abc5",position="QB",team=team1)
        
        team1.save()
        p1.save()
        p2.save()
        p3.save()
        p4.save()
        p5.save()
        
        #Wrong position
        self.assertEqual(play(p2,"QB"),False)
        self.assertEqual(p2.benched,True)
        self.assertEqual(team1.qb_count,1)
        
        #Already playing
        self.assertEqual(play(p1,"WR"),False)
        self.assertEqual(p1.benched,False)
        self.assertEqual(team1.wr_count,1)
        
        #Not on a team
        self.assertEqual(play(p3,"WR"),False)
        self.assertEqual(p3.team, None)
        self.assertEqual(p3.benched, True)
        self.assertEqual(team1.wr_count,1)
        
        #2 QB's at the same time
        self.assertEqual(play(p5,"QB"),False)
        self.assertEqual(p4.benched, False)
        self.assertEqual(p5.benched, True)
        self.assertEqual(team1.qb_count,1)
        
        #2 WR's at the same time (valid)
        self.assertEqual(play(p2,"WR"),True)
        self.assertEqual(p2.benched, False)
        self.assertEqual(team1.wr_count,2)

    def bench_test(self):
        User.objects.create_user("dillen", "der2127@columbia.edu", "letmein")
        
        team1 = Team(team_name="Winners",owner=User.objects.get(username__exact="dillen"))

        p1 = Player(full_name="abc1",position="WR",team=team1,benched=False)
        p2 = Player(full_name="abc2",position="WR",team=team1,benched=False)
        team1.wr_count = 2
        p3 = Player(full_name="abc3",position="WR",team=team1)
        p4 = Player(full_name="abc4",position="WR")
        
        team1.save()
        p1.save()
        p2.save()
        p3.save()
        p4.save()
        
        #Bench someone already benched
        self.assertEqual(bench(p3),False)
        self.assertEqual(team1.wr_count,2)
        self.assertEqual(p3.benched,True)
        
        #Bench someone not on a team
        self.assertEqual(bench(p4),False)
        self.assertEqual(team1.wr_count,2)
        self.assertEqual(p4.benched,True)
        
        #Bench a WR
        self.assertEqual(bench(p2),False)
        self.assertEqual(team1.wr_count,1)
        self.assertEqual(p1.benched,False)
        self.assertEqual(p2.benched,True)