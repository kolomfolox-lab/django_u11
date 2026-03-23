from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

def post_list(request):
    q = request.GET.get('q', '')
    if q:
        posts = Post.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 5) # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/list.html', {'page_obj': page_obj})

@permission_required('posts.add_post')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'posts/form.html', {'form': form})

@permission_required('posts.change_post')
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/form.html', {'form': form})

@permission_required('posts.delete_post')
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'posts/confirm_delete.html', {'post': post})
