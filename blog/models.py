from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.CharField(max_length=50, choices=[
        ('ARI', 'Arizona Diamondbacks'),
        ('ATL', 'Atlanta Braves'),
        ('BAL', 'Baltimore Orioles'),
        ('BOS', 'Boston Red Sox'),
        ('CHC', 'Chicago Cubs'),
        ('CWS', 'Chicago White Sox'),
        ('CIN', 'Cincinnati Reds'),
        ('CLE', 'Cleveland Guardians'),
        ('COL', 'Colorado Rockies'),
        ('DET', 'Detroit Tigers'),
        ('HOU', 'Houston Astros'),
        ('KC', 'Kansas City Royals'),
        ('LAA', 'Los Angeles Angels'),
        ('LAD', 'Los Angeles Dodgers'),
        ('MIA', 'Miami Marlins'),
        ('MIL', 'Milwaukee Brewers'),
        ('MIN', 'Minnesota Twins'),
        ('NYM', 'New York Mets'),
        ('NYY', 'New York Yankees'),
        ('OAK', 'Oakland Athletics'),
        ('PHI', 'Philadelphia Phillies'),
        ('PIT', 'Pittsburgh Pirates'),
        ('SD', 'San Diego Padres'),
        ('SF', 'San Francisco Giants'),
        ('SEA', 'Seattle Mariners'),
        ('STL', 'St. Louis Cardinals'),
        ('TB', 'Tampa Bay Rays'),
        ('TEX', 'Texas Rangers'),
        ('TOR', 'Toronto Blue Jays'),
        ('WSH', 'Washington Nationals'),
        ('Other', 'Other'),
    ])

    def get_favorite_team(self):
        return self.favorite_team

    def __str__(self):
        return f"{self.user.username} - {self.favorite_team}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    upvotes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    tags = models.CharField(max_length=200, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def was_published_recently(self):
        """
        Check if post was published within the past day
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)