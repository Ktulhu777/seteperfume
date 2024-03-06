from django.urls import path
from men import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>', views.PostDetailView.as_view(), name='post'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:cat_slug>/', views.CategoryView.as_view(), name='category'),
]
