from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, PostForm
from .models import Post, UserProfile, Comment, IpAddress, Team, Sport

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.error_messages)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, favorite_team=form.cleaned_data['favorite_team'])
            login(request, user)
            return redirect('blog:post_list')
        else:
            return render(request, "blog/signup.html", {"form":form})
        
    else: # GET request
        form = SignUpForm()
        return render(request, 'blog/signup.html', {'form': form})

@login_required(login_url='/accounts/login')
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('blog:post_list')
    else: # GET request
        form = PostForm()
        return render(request, 'blog/dashboard.html', {'form': form, 'posts': posts})

def logout_view(request):
    logout(request)
    return redirect('post_list')


def post_list(request):
    query = request.GET.get('q')
    mlb_teams = Team.objects.filter(sport__name='MLB')

    if query and query == 'oldest':
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

    if posts.count() == 0:
        return render(request, 'blog/post_list.html', {
            'posts': [],
            'teams': mlb_teams,
            'message': "No posts are available."
        })
    else:
        return render(request, 'blog/post_list.html', {
            'posts': posts,
            'teams': mlb_teams,
            'message': ""
        })


def post_detail(request, blog_slug):
    post = get_object_or_404(Post, slug=blog_slug)
    if request.method == "GET":
        ip = get_client_ip(request)
        if IpAddress.objects.filter(ip_address=ip).exists():
            post.views.add(IpAddress.objects.get(ip_address=ip))
        else:
            IpAddress.objects.create(ip_address=ip)
            post.views.add(IpAddress.objects.get(ip_address=ip))
    return render(request, 'blog/post_detail.html', {
        'post': post
    })


def upvote(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if request.user in post.upvotes.all():
            post.upvotes.remove(request.user)
        else:
            post.upvotes.add(request.user)
        return HttpResponseRedirect(reverse("blog:post_detail", args=(post.slug,)))
    else:
        return redirect('blog:signup')


def comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'POST':
            text = request.POST.get('comment')
            print(f"The new comment is: {text}")
            Comment.objects.create(post=post, user=request.user, text=text)
            return HttpResponseRedirect(reverse("blog:post_detail", args=(post.slug,)))
    else:
        return redirect('blog:signup')
    
def team_view(request, team_slug):
    team = Team.objects.get(slug=team_slug)
    if not team:
        return HttpResponseNotFound("Team not found.")
    
    return render(request, 'blog/teams.html', {
        'team': team,
    })