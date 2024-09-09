from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Home page to add a book
    path('book/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('author/edit/<int:pk>/', views.edit_author, name='edit_author'),
    path('author/delete/<int:pk>/', views.delete_author, name='delete_author'),
    path('signup/', views.signup, name='signup'),  
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'),
    path('client/', views.client_page, name='client_page'),
]