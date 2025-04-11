from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from .models import Expense, Budget, Category
from .forms import ExpenseForm, BudgetForm, CategoryForm
from datetime import datetime, timedelta
from django.db.models import Sum
import json

@login_required
def dashboard(request):
    today = datetime.now()
    month_start = today.replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    # Get last 30 days for trend chart
    thirty_days_ago = today - timedelta(days=30)

    monthly_expenses = Expense.objects.filter(
        user=request.user,
        date__range=[month_start, month_end]
    )

    # Get active budgets
    active_budgets = Budget.objects.filter(
        user=request.user,
        start_date__lte=today,
        end_date__gte=today
    )

    # Prepare budget data for chart
    budget_names = []
    budget_amounts = []
    spent_amounts = []
    
    for budget in active_budgets:
        budget_names.append(budget.name)
        budget_amounts.append(float(budget.amount))
        spent_amounts.append(float(budget.get_spent_amount()))
    
    # Prepare category data for chart
    expenses_by_category = monthly_expenses.values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    category_names = [item['category__name'] for item in expenses_by_category]
    category_amounts = [float(item['total']) for item in expenses_by_category]
    
    # Prepare expense trend data
    expense_trend = Expense.objects.filter(
        user=request.user,
        date__range=[thirty_days_ago, today]
    ).values('date').annotate(
        daily_total=Sum('amount')
    ).order_by('date')
    
    trend_dates = [item['date'].strftime('%Y-%m-%d') for item in expense_trend]
    trend_amounts = [float(item['daily_total']) for item in expense_trend]

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

        # Chart data
        'budget_names_json': json.dumps(budget_names),
        'budget_amounts_json': json.dumps(budget_amounts),
        'spent_amounts_json': json.dumps(spent_amounts),
        'category_names_json': json.dumps(category_names),
        'category_amounts_json': json.dumps(category_amounts),
        'trend_dates_json': json.dumps(trend_dates),
        'trend_amounts_json': json.dumps(trend_amounts),
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

