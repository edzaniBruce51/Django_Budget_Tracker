from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'finances'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', LoginView.as_view(template_name='finances/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='finances:login'), name='logout'),
    path('register/', views.register, name='register'),

    # Expense routes
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_create, name='expense_create'),
    path('expenses/edit/<int:pk>/', views.expense_edit, name='expense_edit'),
    path('expenses/delete/<int:pk>/', views.expense_delete, name='expense_delete'),

    # Budget routes
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_create, name='budget_create'),

    # Category routes
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
]
