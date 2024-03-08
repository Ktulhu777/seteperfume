from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView

from men.forms import ReviewForm
from men.models import Perfume, Basket, Review
from men.utils import DataMixin


class HomeView(DataMixin, ListView):
    """Класс отображения главной страницы"""
    title_page = 'Главная страница'
    template_name = 'men/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Perfume.published.all()


class PostDetailView(DataMixin, DetailView, CreateView):
    """Отображение отдельного товара"""
    template_name = 'men/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.get_reviews(context['post'].id)
        return self.get_mixin_context(context, title=context['post'].title, reviews=reviews)

    def get_object(self, queryset=None):
        return get_object_or_404(Perfume.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_reviews(self, slug_url_kwarg):
        return Review.objects.filter(product_review=slug_url_kwarg)

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class CategoryView(DataMixin, ListView):
    """Класс для отображения категории на главной страницы"""
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


class BasketView(LoginRequiredMixin, DataMixin, ListView):
    """Класс отображения корзины"""
    title_page = 'Корзина'
    template_name = 'men/basket.html'
    context_object_name = 'baskets'

    def get_queryset(self):
        user = self.request.user
        return Basket.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        baskets = Basket.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        total_amount = sum(basket.total_amount() for basket in baskets)
        total_quantity = sum(basket.quantity for basket in baskets)
        return self.get_mixin_context(context, total_amount=total_amount, total_quantity=total_quantity)


@login_required(redirect_field_name='home')
def basket_add(request, post_slug):
    """Функция представления для добавления продукта в корзину
    и для увеличения количества продуктов в корзине """
    your_page = request.META.get("HTTP_REFERER")
    product = Perfume.objects.get(slug=post_slug)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():  # Если корзины нет, то мы ее формируем
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return redirect(your_page)
    else:  # Добавляем количество товаров
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return redirect(your_page)


def basket_del(request, id_product):
    """Удаляем товар полностью с корзины """
    basket = Basket.objects.get(pk=id_product)
    basket.delete()
    return redirect(request.META.get("HTTP_REFERER"))


class SearchView(DataMixin, ListView):
    """Класс для поиска парфюмов"""
    template_name = 'men/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Perfume.published.filter(title__contains=self.request.GET.get('search'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        return self.get_mixin_context(context)
