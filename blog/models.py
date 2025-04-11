from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django_ckeditor_5.fields import CKEditor5Field
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
    
class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=200, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, default='')
    tags = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200)
    text = CKEditor5Field('Text', config_name='extends', null=False)
    upvotes = models.ManyToManyField(User, related_name='upvotes', blank=True)
    views = models.ManyToManyField(IpAddress, related_name='views', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_text = self.title + " " + str(self.author.id)
            self.slug = slugify(slug_text)
        super(Post, self).save(*args, **kwargs)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def was_published_recently(self):
        """
        Check if post was published within the past day
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now
    
    def number_of_upvotes(self):
        return self.upvotes.count()
    
    def number_of_views(self):
        return self.views.count()
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = CKEditor5Field('Text', config_name='extends', null=False)
    created_date = models.DateTimeField(default=timezone.now)

class Sport(models.Model):
    name = models.CharField(max_length=50, choices=[
        ('MLB', 'Major League Baseball'),
    ])
    logo_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=3)
    slug = models.SlugField(max_length=50, default='', blank=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    logo_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Leaderboard(models.Model):
    # This model will track the users with the most upvotes on their posts
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    upvotes = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-upvotes']

    def update_upvotes(self):
        self.upvotes = Post.objects.filter(author=self.user).aggregate(Sum('upvotes'))['upvotes__sum'] or 0
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.upvotes}"