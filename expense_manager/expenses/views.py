from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Expense
from .serializers import ExpenseSerializer
from .logging import log_request_and_exception
from datetime import datetime

class ExpenseListView(APIView):
    """
    Handle listing all expenses and creating a new expense.
    """
    @log_request_and_exception
    def get(self, request):
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    @log_request_and_exception
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    """
    Handle retrieving and deleting a single expense.
    """
    @log_request_and_exception
    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    @log_request_and_exception
    def delete(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseByDateRangeView(APIView):
    """
    Handle listing expenses for a specific user within a given date range.
    """
    @log_request_and_exception
    def get(self, request, user_id):
        start_date = request.query_params.get('start')
        end_date = request.query_params.get('end')

        if not start_date or not end_date:
            return Response({"error": "Both start and end dates are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        expenses = Expense.objects.filter(user_id=user_id, date__range=[start_date, end_date])
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)


class ExpenseCategorySummaryView(APIView):
    """
    Handle summarizing expenses by category for a specific user and month.
    """
    @log_request_and_exception
    def get(self, request, user_id, month):
        try:
            month = int(month)
            if month < 1 or month > 12:
                return Response({"error": "Month must be between 1 and 12."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Invalid month format. Use an integer (1-12)."}, status=status.HTTP_400_BAD_REQUEST)

        expenses = Expense.objects.filter(user_id=user_id, date__month=month)
        if not expenses.exists():
            return Response({"message": "No expenses found for the specified month."}, status=status.HTTP_404_NOT_FOUND)

        summary = expenses.values('category').annotate(total=Sum('amount'))
        return Response(summary)