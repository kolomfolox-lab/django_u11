from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post
from django.db.models import Q

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
