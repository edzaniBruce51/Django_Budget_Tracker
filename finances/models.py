from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Category(models.Model):
    """Represents a spending category that helps organize expenses and budgets.
    Each category belongs to a specific user for data isolation."""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_total_expenses(self):
        """Returns the total expenses for this category"""
        return self.expense_set.aggregate(total=Sum('amount'))['total'] or 0

class Budget(models.Model):
    """Represents a spending budget for a specific category and time period.
    Tracks planned vs actual spending to help users manage their finances."""
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

    def get_spent_amount(self):
        """Calculates total spent amount within budget period and category"""
        return Expense.objects.filter(
            user=self.user,
            category=self.category,
            date__range=[self.start_date, self.end_date]
        ).aggregate(total=Sum('amount'))['total'] or 0

    def get_remaining_amount(self):
        """Calculates remaining budget amount"""
        return self.amount - self.get_spent_amount()

    def get_percentage_used(self):
        """Calculates percentage of budget used"""
        spent = self.get_spent_amount()
        return (spent / self.amount * 100) if self.amount > 0 else 0

class Expense(models.Model):
    """Represents an individual expense entry.
    Tracks amount, date, description, and category for expense tracking."""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['category', 'date'])
        ]

    def __str__(self):
        return f"{self.description} (${self.amount} on {self.date})"
