from django.shortcuts import render, get_object_or_404
from django.core.signing import BadSignature
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q

from .utilities import signer
from .forms import SearchForm, GuestCommentForm, UserCommentForm
from .models import AdvancedUser, Post, PostCategory, Comment


# My views
def user_activation(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'email/bad_signature.html')
    user = get_object_or_404(AdvancedUser, username=username)
    if user.is_activated:
        template = 'registration/user_is_activated'
    else:
        template = 'registration/activation_done.html'
        user.is_activate = True
        user.is_activated = True
        user.save()
    return render(request, template)


def get_search_result(request, posts):
    """Возвращает страницу с постами и форму поиска"""
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        posts = posts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    paginator = Paginator(posts, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    return page, form


def index(request):
    posts = Post.objects.filter(is_active=True)[:10]
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
        posts = posts.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    context = {'posts': posts}
    return render(request, 'blog/index.html', context)


def by_category(request, pk):
    category = get_object_or_404(PostCategory, pk=pk)
    posts = Post.objects.filter(is_active=True, category=pk)
    page, form = get_search_result(request, posts)
    context = {'category': category, 'page': page, 'posts': page.object_list, 'form': form}
    return render(request, 'blog/by_category.html', context)


def detail(request, category_pk, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=pk, is_active=True)
    initial = {'post': post.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        c_form = form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request, messages.SUCCESS, 'Комментарий добавлен')
        else:
            form = c_form
            messages.add_message(request, messages.WARNING, 'Комментарий не добавлен')
    context = {'post': post, 'comments': comments, 'form': form}
    return render(request, 'blog/detail.html', context)
