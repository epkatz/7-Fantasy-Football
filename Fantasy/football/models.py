from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.related import ForeignKey

#Team
class Team(models.Model):
    team_name = models.CharField(max_length=50)
    current_rank = models.IntegerField(max_length=2, default = 0)
    owner = ForeignKey(User)
    size = models.IntegerField(max_length=2,default=0)
    total_pts = models.IntegerField(default=0)
    budget = models.IntegerField(default=100)
    
    qb_count = models.IntegerField(default=0)
    rb_count = models.IntegerField(default=0)
    wr_count = models.IntegerField(default=0)
    pk_count = models.IntegerField(default=0)
    st_count = models.IntegerField(default=0)
    te_count = models.IntegerField(default=0)
    
    week1 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week2 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week3 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week4 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week5 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week6 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week7 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week8 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week9 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week10 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week11 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week12 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week13 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week14 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week15 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week16 = models.IntegerField(blank=True, null=True, editable=False, default=0)

    def __unicode__(self):
        return u'%s' % (self.team_name)
    
    """
    #If we have time then we can add extra validation - @Eli
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.qb.position != 'QB':
            raise ValidationError('QB Position must be occupied by a QB')
    """

#Players
class Player(models.Model):
    full_name = models.CharField(max_length=70)
    POSITION_CHOICES = (
        ('QB', 'QB'),
        ('RB', 'RB'),
        ('WR', 'WR'),
        ('PK', 'PK'),
        ('ST', 'ST'),
        ('TE', 'TE'),
    )
    total_pts = models.IntegerField(default=0)
    average_pts = models.DecimalField(decimal_places=2, max_digits=4, default=0)
    position = models.CharField(max_length=2)
    salary = models.IntegerField(max_length=2)
    benched = models.BooleanField(default=True)
    team = ForeignKey('Team', blank=True, null=True) 
    
    week1 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week2 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week3 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week4 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week5 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week6 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week7 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week8 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week9 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week10 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week11 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week12 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week13 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week14 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week15 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    week16 = models.IntegerField(blank=True, null=True, editable=False, default=0)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.full_name, self.position)
    
    def is_free_agent(self):
        return self.team is None
    
#Scoring
class Scoring(models.Model):
    action = models.CharField(max_length=20)
    points = models.IntegerField()
    def __unicode__(self):
        return u'%s' % (self.action)
    
class Trade(models.Model):
    tid = models.IntegerField()
    team_from = ForeignKey(Team, related_name='Team1')
    team_to = ForeignKey(Team, related_name='Team2')
    player = ForeignKey(Player, related_name='Player')
    proposed_trade = ForeignKey(Team, related_name='Proposed_Trade')
    to_approve = ForeignKey(Team, related_name='To_Approve')
    
class Task(models.Model):

    class Meta:
        permissions = (
            ("add_week", "Can upload stats"),
        )
