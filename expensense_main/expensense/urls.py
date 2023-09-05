from django.urls import path
from expensense.views import *

app_name = 'expensense'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register_step1/', RegisterStep1View.as_view(), name='registration_step1'),
    path('register_step2/', RegistrationStep2View.as_view(), name='registration_step2'),
    path('register_step2/teams/', teams, name='teams'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('log_expense/', LogExpenseView.as_view(), name='log_expense'),
    path('log_expense/ocr_api/', OcrApiView.as_view(), name='ocr_api'),
    path('expenses/', AllExpenseView.as_view(), name='expenses'),
    path('approval_conditions/', ApprovalConditionView.as_view(), name='approval_conditions'),
    path('set_approval_conditions/', SetApprovalConditions.as_view(), name='set_approval_conditions'),
    path('pending_expense_requests/', PendingRequestView.as_view(), name='pending_exp_req'),
    path('pending_expense_requests/<int:expense_id>/', ExpenseView.as_view(), name='expense_details'),
    path('approve_expense/<int:expense_id>/', ApproveExpenseView.as_view(), name='approve_expense'),
    path('deny_expense/<int:expense_id>/', DenyExpenseView.as_view(), name='deny_expense'),
    path('generate_expense_pdf/', GenerateExpensePDFView.as_view(), name='generate_expense_pdf'),
    path('generate_expense_pdf/<str:start_date>/<str:end_date>/', GenerateExpensePDFView.as_view(), name='generate_monthly_expense_pdf'),
    path('budgets/', BudgetView.as_view(), name='budget'),
]