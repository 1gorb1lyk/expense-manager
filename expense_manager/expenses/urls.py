from django.urls import path
from .views import (
    ExpenseListView,
    ExpenseDetailView,
    ExpenseByDateRangeView,
    ExpenseCategorySummaryView
)

urlpatterns = [
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/date-range/<int:user_id>/', ExpenseByDateRangeView.as_view(), name='expenses-date-range'),
    path('expenses/summary/<int:user_id>/<int:month>/', ExpenseCategorySummaryView.as_view(), name='category-summary'),
]