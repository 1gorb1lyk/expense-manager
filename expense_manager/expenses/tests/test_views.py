from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime
from expenses.models import User, Expense


class ExpenseAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(username="testuser", email="test@example.com")

        # Create some sample expenses
        self.expense1 = Expense.objects.create(
            user=self.user,
            title="Lunch",
            amount=15.5,
            date="2024-11-10",
            category="Food"
        )
        self.expense2 = Expense.objects.create(
            user=self.user,
            title="Taxi",
            amount=30.0,
            date="2024-11-11",
            category="Travel"
        )
        self.expense3 = Expense.objects.create(
            user=self.user,
            title="Electricity Bill",
            amount=75.5,
            date="2024-11-01",
            category="Utilities"
        )

    def test_create_expense(self):
        url = reverse('expense-list')
        data = {
            "user": self.user.id,
            "title": "Groceries",
            "amount": 50,
            "date": "2024-11-12",
            "category": "Food"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "Groceries")
        self.assertEqual(response.data['amount'], '50.00')

    def test_list_expenses(self):
        url = reverse('expense-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_expense(self):
        url = reverse('expense-detail', args=[self.expense1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Lunch")

    def test_delete_expense(self):
        url = reverse('expense-detail', args=[self.expense1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense1.id).exists())

    def test_expenses_by_date_range(self):
        url = reverse('expenses-date-range', args=[self.user.id])
        response = self.client.get(url, {'start': '2024-11-01', 'end': '2024-11-11'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_category_summary(self):
        url = reverse('category-summary', args=[self.user.id, 11])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item['category'] == 'Food' for item in response.data))
        self.assertTrue(any(item['category'] == 'Travel' for item in response.data))

    def test_invalid_amount(self):
        url = reverse('expense-list')
        data = {
            "user": self.user.id,
            "title": "Invalid Expense",
            "amount": -100,
            "date": "2024-11-12",
            "category": "Food"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)