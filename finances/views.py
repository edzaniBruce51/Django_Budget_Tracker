from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from .models import Expense, Budget, Category
from .forms import ExpenseForm, BudgetForm, CategoryForm
from datetime import datetime, timedelta
from django.db.models import Sum

@login_required
def dashboard(request):
    today = datetime.now()
    month_start = today.replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__range=[month_start, month_end]
    )

    context = {
        'total_expenses': monthly_expenses.aggregate(total=Sum('amount'))['total'] or 0,
        'active_budgets': Budget.objects.filter(
            user=request.user,
            start_date__lte=today,
            end_date__gte=today
        ),
        'expenses_by_category': monthly_expenses.values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total'),
        'recent_expenses': monthly_expenses.order_by('-date')[:5],
    }
    return render(request, 'finances/dashboard.html', context)

# Expense views
@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'finances/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('finances:expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'finances/expense_form.html', {'form': form})

@login_required
def expense_edit(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated successfully!')
            return redirect('finances:expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'finances/expense_form.html', {'form': form, 'expense': expense})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted successfully!')
        return redirect('finances:expense_list')
    return render(request, 'finances/expense_confirm_delete.html', {'expense': expense})

# Budget views
@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'finances/budget_list.html', {'budgets': budgets})

@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('finances:budget_list')
    else:
        form = BudgetForm()
    return render(request, 'finances/budget_form.html', {'form': form})

# Category views
@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'finances/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('finances:category_list')
    else:
        form = CategoryForm()
    return render(request, 'finances/category_form.html', {'form': form})

# Authentication view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('finances:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'finances/register.html', {'form': form})
