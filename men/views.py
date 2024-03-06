from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from men.models import Perfume
from men.utils import DataMixin


class HomeView(DataMixin, ListView):
    title_page = 'Главная страница'
    template_name = 'men/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Perfume.published.all()


class PostDetailView(DataMixin, DetailView):
    template_name = 'men/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Perfume.published, slug=self.kwargs[self.slug_url_kwarg])


class CategoryView(DataMixin, ListView):
    template_name = 'men/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Perfume.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.cat_name)


def about(request):
    return HttpResponse('О сайте')


def contact(request):
    return HttpResponse('Обратная связь')
