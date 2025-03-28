from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post

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

