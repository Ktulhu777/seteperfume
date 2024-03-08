from django.urls import path
from men import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.PostDetailView.as_view(), name='post'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:cat_slug>/', views.CategoryView.as_view(), name='category'),
    path('basket-user/', views.BasketView.as_view(), name='basket'),
    path('product-add/<slug:post_slug>/', views.basket_add, name='basket_add'),
    path('product-del/<int:id_product>/', views.basket_del, name='basket_del'),
    path('search/', views.SearchView.as_view(), name='search'),
]
