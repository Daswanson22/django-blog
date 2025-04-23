from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum, Count
from django_ckeditor_5.fields import CKEditor5Field
import datetime

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
    stadium_url = models.URLField(blank=True, null=True, default="")
    stadium_alt = models.CharField(max_length=50, blank=True, null=True, default="")
    
    def total_team_post_upvotes(self):
        return Post.objects.filter(author__userprofile__favorite_team=self).annotate(upvote_count=Count('upvotes')).aggregate(total=Sum('upvote_count'))['total'] or 0

    def total_team_posts(self):
        return Post.objects.filter(author__userprofile__favorite_team=self).count()

    def total_team_comments(self):
        return Comment.objects.filter(user__userprofile__favorite_team=self).count()

    def total_team_comment_upvotes(self):
        return Comment.objects.filter(user__userprofile__favorite_team=self).annotate(upvote_count=Count('upvotes')).aggregate(total=Sum('upvote_count'))['total'] or 0
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    def get_favorite_team(self):
        return self.favorite_team
    
    def total_post_upvotes(self):
        return Post.objects.filter(author=self.user).annotate(upvote_count=Count('upvotes')).aggregate(total=Sum('upvote_count'))['total'] or 0

    def total_posts(self):
        return Post.objects.filter(author=self.user).count()

    def total_comments(self):
        return Comment.objects.filter(user=self.user).count()

    def total_comment_upvotes(self):
        # Requires adding upvotes to Comment model (see below)
        return Comment.objects.filter(user=self.user).annotate(upvote_count=Count('upvotes')).aggregate(total=Sum('upvote_count'))['total'] or 0

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
    upvotes = models.ManyToManyField(User, related_name='comment_upvotes', blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def number_of_upvotes(self):
        return self.upvotes.count()

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