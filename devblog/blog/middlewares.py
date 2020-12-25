from .models import PostCategory
from .forms import SearchForm


def blog_context_processor(request):
    context = {}
    context['categories'] = PostCategory.objects.all()
    context['keyword'] = ''
    context['all'] = ''
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    else:
        keyword = ''
    form = SearchForm(initial={'keyword': keyword})
    context['form'] = form
    if 'page' in request.GET:
        page = request.GET['page']
        if page != '1':
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page
    return context
