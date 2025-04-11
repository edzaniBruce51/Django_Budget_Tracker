from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Expense, Budget
from decimal import Decimal
from datetime import date, timedelta

class FinanceTests(TestCase):
    def setUp(self):
        # Create test user
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description',
            user=self.user
        )

        # Create test expense
        self.expense = Expense.objects.create(
            description='Test Expense',
            amount=Decimal('50.00'),
            date=date.today(),
            category=self.category,
            user=self.user
        )

        # Create test budget
        self.budget = Budget.objects.create(
            name='Test Budget',
            amount=Decimal('1000.00'),
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            category=self.category,
            user=self.user
        )

    def test_user_authentication(self):
        # Test login
        login = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login)

        # Test accessing protected page
        response = self.client.get(reverse('finances:dashboard'))
        self.assertEqual(response.status_code, 200)

        # Test logout
        self.client.logout()
        response = self.client.get(reverse('finances:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirects to login

    def test_expense_operations(self):
        self.client.login(username='testuser', password='testpass123')

        # Test expense list
        response = self.client.get(reverse('finances:expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Expense')

        # Test expense creation
        new_expense_data = {
            'description': 'New Expense',
            'amount': '75.00',
            'date': date.today(),
            'category': self.category.id
        }
        response = self.client.post(reverse('finances:expense_create'), new_expense_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Expense.objects.filter(description='New Expense').exists())

        # Test expense edit
        edit_expense_data = {
            'description': 'Edited Expense',
            'amount': '60.00',
            'date': date.today(),
            'category': self.category.id
        }
        response = self.client.post(reverse('finances:expense_edit', args=[self.expense.id]), edit_expense_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Expense.objects.filter(description='Edited Expense').exists())

        # Test expense deletion
        response = self.client.post(reverse('finances:expense_delete', args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())

    def test_budget_operations(self):
        self.client.login(username='testuser', password='testpass123')

        # Test budget list
        response = self.client.get(reverse('finances:budget_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Budget')

        # Test budget creation
        new_budget_data = {
            'name': 'New Budget',
            'amount': '500.00',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=30),
            'category': self.category.id
        }
        response = self.client.post(reverse('finances:budget_create'), new_budget_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Budget.objects.filter(name='New Budget').exists())

    def test_category_operations(self):
        self.client.login(username='testuser', password='testpass123')

        # Test category list
        response = self.client.get(reverse('finances:category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

        # Test category creation
        new_category_data = {
            'name': 'New Category',
            'description': 'New Description'
        }
        response = self.client.post(reverse('finances:category_create'), new_category_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='New Category').exists())

    def test_dashboard(self):
        self.client.login(username='testuser', password='testpass123')

        # Test dashboard access and content
        response = self.client.get(reverse('finances:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Expense')
        self.assertContains(response, 'Test Budget')

        # Test dashboard calculations
        context = response.context
        self.assertEqual(context['total_expenses'], Decimal('50.00'))
        self.assertEqual(len(context['active_budgets']), 1)
        self.assertEqual(len(context['recent_expenses']), 1)
