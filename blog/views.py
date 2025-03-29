from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, PostForm
from .models import Post, UserProfile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            UserProfile.objects.create(user=user, favorite_team=form.cleaned_data['favorite_team'])
            login(request, user)
            return redirect('post_list')
        # else:
        #     return HttpResponseNotFound()
    else: # GET request
        form = SignUpForm()
        return render(request, 'blog/signup.html', {'form': form})

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_date')
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else: # GET request
        form = PostForm()
        return render(request, 'blog/dashboard.html', {'form': form, 'posts': posts})

def post_list(request):
    query = request.GET.get('q')
    post = None
    if query and query == 'oldest':
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {
        'posts': posts
    })

def post_detail(request, pk):
    print(pk)
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {
        'post': post
    })

