from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views import View
from expensense.models import *
from django.contrib.auth import login, authenticate, logout
from expensense.forms import *
from django.utils import timezone
import json
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from expensense.ocr_api import results
from django.utils.datastructures import MultiValueDictKeyError
import tempfile
from tempfile import NamedTemporaryFile
import os
from django.core.files.uploadedfile import InMemoryUploadedFile
from expensense.signature_matching import calculate_similarity

from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.db.models.functions import TruncMonth

from datetime import datetime, timedelta
from expensense.report import generate_pdf


class IndexView(View):
    """Class for index page"""

    def get(self, request):
        """ Method to get the index page"""

        return render(request, 'expensense/index.html')


class RegisterStep1View(View):
    """ Class to handle the first step of registration """

    def get(self, request):
        """ Method to handle the get request """
        form = Step1Form()
        return render(request, 'expensense/register_step_1.html', {'form': form})

    def post(self, request):
        """ Method to handle the form submission and storing data in session """
        form = Step1Form(request.POST, request.FILES)

        if form.is_valid():
            step1_data = form.cleaned_data.copy()
             # Handle the uploaded file
            uploaded_file = request.FILES.get('signature')
            if uploaded_file:
                # Create a temporary file to store the uploaded file's contents
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(uploaded_file.read())
                    step1_data['signature'] = temp_file.name

            # Store step 1 data in the session
            request.session['step1_data'] = step1_data

            # Redirect to Step 2
            return redirect('expensense:registration_step2')
        else:
            form = Step1Form(request.POST)
            return render(request, 'expensense/register_step_1.html', {'form': form})


class RegistrationStep2View(View):
    """ Class to handle the second step of the registration process """

    def get_form(self, role):
        """ Method to select step 2 form based on role selected """
        if role == 'ADM':
            return Step2FormAdmin()
        elif role == 'MNG':
            return Step2FormManager()
        elif role == 'EMP':
            return Step2FormEmployee()
        else:
            return None

    def get(self, request):
        """ Method to handle get request """
        step1_data = request.session.get('step1_data')
        if step1_data is None:
            return redirect('expensense:registration_step1')

        form = self.get_form(step1_data.get('role'))
        if not form:
            return redirect('expensense:registration_step1')

        return render(request, 'expensense/register_step_2.html',
                      {'form': form, 'role': step1_data.get('role')})

    def post(self, request):
        """ Method to handle the submission for step-2 form """
        step1_data = request.session.get('step1_data')
        if step1_data is None:
            return redirect('expensense:registration_step1')

        form = self.get_form(step1_data.get('role'))
        if not form:
            return redirect('expensense:registration_step1')

        # Use Step 1 data to determine which Step 2 form to display
        if step1_data.get('role') == 'ADM':
            form = Step2FormAdmin(request.POST)
        elif step1_data.get('role') == 'MNG':
            form = Step2FormManager(request.POST)
        elif step1_data.get('role') == 'EMP':
            form = Step2FormEmployee(request.POST)

        if form.is_valid():
            step2_data = form.cleaned_data
            # Check for different roles selected in step 1 and perform
            # different opperations
            if step1_data['role'] == 'ADM':
                # if Admin then create a company, add the categories selected
                #  and create an admin team for that company
                categories_from_form = step2_data.get('categories')
                company = Company.objects.create(
                    company=step2_data.get('company'),
                    company_budget=step2_data.get('company_budget')
                )
                company.add(categories_from_form)
                company.save()

                Team.objects.create(company=Company.objects.get(
                    company=step2_data.get('company')),team_name='Admin')

            elif step1_data.get('role') == 'MNG':
                # if the role is manager then create a team
                team = Team.objects.create(
                    company=Company.objects.get(
                        company=step2_data.get('company')),
                    team_name=step2_data.get('team_name'),
                    team_budget=step2_data.get('team_budget')
                )
                team.save()

            # get the company object selected
            company_obj = Company.objects.get(
                company=step2_data.get('company'))

            # if the role is not admin then get the team object based on the
            # company and team selected else the team will be admin in that
            # company
            if step1_data['role'] != 'ADM':
                team_obj = Team.objects.get(
                    company=company_obj, team_name=step2_data.get('team_name'))
            else:
                team_obj = Team.objects.get(team_name='Admin', 
                                            company=Company.objects.get(
                    company=step2_data.get('company')))

            # Get the path of the temporary file from step1_data
            temp_file_path = step1_data.get('signature')

            if temp_file_path:
                # Open the temporary file and read its contents
                with open(temp_file_path, 'rb') as temp_file:
                    
                    image_file = InMemoryUploadedFile(
                        temp_file, None, 'signature.jpg', 'image/jpeg',
                        temp_file.tell(), None
                    )
                    # Create the user object with the selected form inputs and
                    # company and team objects
                    user = User.objects.create(
                        username=step1_data['username'],
                        email=step1_data['email'],
                        password=make_password(step1_data['password']),
                        first_name=step1_data['first_name'],
                        last_name=step1_data['last_name'],
                        role=step1_data['role'],
                        company_id=company_obj.id,
                        team_id=team_obj.id,
                    )
                    user.signature = image_file
                    user.save()
            # Delete the temporary file after using it
            os.unlink(temp_file_path)

            del temp_file_path
            # delete the session data
            del request.session['step1_data']
            # save the user instance
            user.save()

            # reditect to the login
            return redirect('expensense:login')
        else:
            if step1_data.get('role') == 'ADM':
                form = Step2FormAdmin(request.POST)
            elif step1_data.get('role') == 'MNG':
                form = Step2FormManager(request.POST)
            elif step1_data.get('role') == 'EMP':
                form = Step2FormEmployee(request.POST)

        return render(request, 'expensense/register_step_2.html',
                      {'form': form, 'role': step1_data.get('role')})


def teams(request):
    """ method to get the team names for a company"""

    # get team objects based on the request body which contains company id
    data = json.loads(request.body)
    teams = Team.objects.filter(company_id=data['comp_id'])

    # return a json response of team id and name
    return JsonResponse(list(teams.values('id', 'team_name')), safe=False)


class LoginView(View):
    ''' Class to handle login requests'''

    def get(self, request):
        ''' Method to handle get requests '''
        return render(request, 'expensense/login.html')

    def post(self, request):
        ''' Method to handle post requests '''
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate the user
        user = authenticate(username=username, password=password)

        # if the user exists and is active log them in else show errors
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('expensense:dashboard'))
            else:
                return HttpResponse('Your Account has been disabled')
        else:
            print(f"Invalid user details: {username}, {password}")
            return HttpResponse('Invalid login details supplied')


class LogoutView(View):
    ''' Class to handle secure logout'''

    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect(reverse('expensense:index'))


class DashboardView(View):
    ''' Class to define dashboard workflow'''

    def expense_graph_view(self, request):
        """ Method to create the graph of the expenditure based on roles in 
        the past year""" 

        today = timezone.now().date()
        one_year = today - timedelta(days=365)

        # Query the expense table for different roles
        if request.user.role == 'ADM':
            all_expenses = Expense.objects.filter(
                Q(user_id__company=request.user.company) & Q(
                expense_date__gte=one_year) & Q(expense_date__lte=today))
        
        elif request.user.role == 'MNG':
            all_expenses = Expense.objects.filter(
                Q(user_id__company=request.user.company) & Q(
                user_id__team=request.user.team) & Q(
                expense_date__gte=one_year) & Q(expense_date__lte=today))
        
        elif request.user.role == 'EMP':
            all_expenses = Expense.objects.filter(Q(user_id=request.user) & Q(
                expense_date__gte=one_year) & Q(expense_date__lte=today))


        # Calculate total expenses for each month
        expenses_by_month = all_expenses.annotate(month=TruncMonth(
            'expense_date')).values('month').annotate(
            total_amount=Sum('amount')).order_by('month')

        # Create a dictionary to store expenses by month
        expenses_dict = {}

        # Fill the dictionary with months in the past year and 0 expenses
        current_month = today.replace(day=1)
        while current_month >= one_year.replace(day=1):
            month_str = current_month.strftime('%b %Y')
            if month_str not in expenses_dict:
                expenses_dict[month_str] = 0
            current_month = current_month - timedelta(days=1)
            current_month = current_month.replace(day=1)

        #change the expense value for the months that had expenses
        for expense in expenses_by_month:
            month_str = expense['month'].strftime('%b %Y')
            expenses_dict[month_str] = float(expense['total_amount'])

        return {
            'expenses': expenses_dict,
        }


    def overall_summary(self, request):
        """ Method to get the overall summary of expenses based on categories """

        today = timezone.now().date()
        one_year = today - timedelta(days=365)

        if request.user.role == 'ADM':
            expenses = Expense.objects.filter(Q(user_id__company=request.user.company) & Q(
                expense_date__gte=one_year) & Q(expense_date__lte=today))
        elif request.user.role == 'MNG':
            expenses = Expense.objects.filter(Q(
                user_id__team=request.user.team) & Q(
                user_id__company=request.user.company) & Q(
                expense_date__gte=one_year) & Q(expense_date__lte=today))
        elif request.user.role == 'EMP':
            expenses = Expense.objects.filter(Q(user_id=request.user) & Q(
                expense_date__gte=one_year) & Q(expense_date__lte=today))
        
        # aggregate the expenses in total and category wise
        total_amount = expenses.aggregate(total_amount=Sum('amount'))['total_amount']
        amounts_by_category = expenses.values('category__category_name').annotate(category_amount=Sum('amount'))

        return total_amount, amounts_by_category

    def pending_requests(self, request):
        """ Method to get pending requests """

        # send back 3 most recent requests based on roles
        if request.user.role == 'ADM':
            # requests that are manager approved and within the same company
            pending = Expense.objects.filter(Q(status=Expense.manager_approved) & Q(
                user_id__company=request.user.company)).order_by('-created_at')[:3]
            return pending

        elif request.user.role == 'MNG':
            # requests that are pending and from the same team and company
            pending = Expense.objects.filter(Q(status=Expense.pending) & Q(
                user_id__team=request.user.team) & Q(
                user_id__company=request.user.company)).order_by('-created_at')[:3]
            return pending
        else:
            # for employee return the requests generated by them
            pending = Expense.objects.filter(Q(status=Expense.pending) & Q(
                user_id=request.user)).order_by('-created_at')[:3]
            return pending

    def approved_requests(self, request):
        """ Method to get the approved requests based on roles """

        if request.user.role == 'ADM':
            # for admin send the approved requests for the company and 
            # status 'admin approved'
            approved = Expense.objects.filter(
                Q(status=Expense.admin_approved) & Q(
                    user_id__company=request.user.company)).order_by('-created_at')[:3]
            return approved

        elif request.user.role == 'MNG':
            # for manager, send the requests approved by them or admin fo
            # their team and their company
            approved = Expense.objects.filter(
                Q(Q(status=Expense.manager_approved) | Q(
                status=Expense.admin_approved)) & Q(
                    user_id__team=request.user.team) & Q(
                user_id__company=request.user.company)
            ).order_by('-created_at')[:3]
            return approved

        else:
            # for employee send the final approved requests which are 
            # generated by them
            approved = Expense.objects.filter(Q(
                status=Expense.admin_approved) & Q(
                user_id=request.user)).order_by('-created_at')[:3]
            return approved

    def get_last_three_reports(self):
        """ Method to get the last three month reports from the date of login """

        today = datetime.today().date()
        last_three_reports = []

        for i in range(3):
            end_date = today.replace(day=1) - timedelta(days=1)
            start_date = end_date.replace(day=1)
            last_three_reports.append(start_date.strftime('%B %Y'))
            today = start_date

        return last_three_reports

    @method_decorator(login_required)
    def get(self, request):
        """method to handle get requests"""
        # create a context dictionary that has all the data required on the
        # dashboard
        context_dict = {}
        context_dict = self.expense_graph_view(request)
        context_dict['total_amount'], context_dict['amounts_by_category'] = self.overall_summary(request)
        context_dict['pending'] = self.pending_requests(request)
        context_dict['approved'] = self.approved_requests(request)
        context_dict['last_three_reports'] = self.get_last_three_reports()
        return render(request, 'expensense/dashboard.html', context_dict)


class LogExpenseView(View):
    """class to handle log expense requests"""

    @method_decorator(login_required)
    def get(self, request):
        """method to get log expense form """
        form = ExpenseForm(user=request.user)

        return render(request, 'expensense/log_expense.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        """ Method to handle post request of expense form"""
        expense_form = ExpenseForm(request.POST, request.FILES, user=request.user)

        if expense_form.is_valid():
            expense = expense_form.save(commit=False)
            # have default status as 0 (Pending)
            status = 0
            # change the status based on the role of the user
            if request.user.role == 'MNG':
                status = 1  # manager approved
            elif request.user.role == 'ADM':
                status = 2  # admin approved
            category_obj = Category.objects.get(id = request.POST.get('category'))
            # run the signature matching before creating an expense object
            # query the user table
            user = User.objects.get(id = request.user.id)
            receipt = request.FILES['receipt']
            if user.signature and receipt:
                with NamedTemporaryFile(delete=False) as temp_receipt_file:
                    temp_receipt_file.write(receipt.read())
                    temp_receipt_file.seek(0)
                    similarity = calculate_similarity(temp_receipt_file.name, user.signature.path)
                expense.similarity = similarity  # Save similarity to the expense instance
            
            # Update or create the expense instance
            expense.user_id = request.user
            expense.status = status
            expense.category = category_obj
            expense.receipt = receipt  # Assign the receipt to the expense
            expense.save()
            # Delete the temporary file after using it
            os.unlink(temp_receipt_file.name)
            # once done redirect to dashboard
            return redirect(reverse('expensense:dashboard'))
        else:
            print(expense_form.errors)

        return self.get(request)


class OcrApiView(View):
    """ This class handles the API call from the template to get expense data from image"""

    def post(self, request):
        """ method to handle the post request """
        try:
            # print(request.FILES['file'])
            file = request.FILES['file']

            # save the file in a temp dir
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, 'wb') as temp_dest:
                for chunk in file.chunks():
                    temp_dest.write(chunk)

            # run the OCR API on the file
            response = results(file_path)
            # remove the temp file and dir
            os.remove(file_path)
            os.rmdir(temp_dir)
            # return response as a json

            return JsonResponse(response, safe=False)
        except MultiValueDictKeyError:
            return JsonResponse({'error': 'File not found in request'}, status=400)


class AllExpenseView(View):
    """ Class to handle expense view for Admin and Manager """

    @method_decorator(login_required)
    def get(self, request):
        """ Method to get the paginated expense details """
        # Query Expense object based on role
        if request.user.role == 'ADM':
            expenses = Expense.objects.filter(
                user_id__company=request.user.company).order_by('-expense_date')

        elif request.user.role == 'MNG':
            query_1 = Q(user_id__company=request.user.company)
            query_2 = Q(user_id__team=request.user.team)
            expenses = Expense.objects.filter(
                query_1 & query_2).order_by('-expense_date')

        elif request.user.role == 'EMP':
            expenses = Expense.objects.filter(
                user_id=request.user).order_by('-expense_date')

        # paginate the objects received
        paginator = Paginator(expenses, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'expensense/expenses.html', {'page_obj': page_obj})


class ApprovalConditionView(View):
    """ Class to get approval conditions """

    @method_decorator(login_required)
    def get(self, request):
        """ Method to get the existing conditions """
        if not request.user.role == 'EMP':
            if request.user.role == 'ADM':
                conditions = ApprovalConditions.objects.filter(user = request.user)
            elif request.user.role == 'MNG':
                conditions = ApprovalConditions.objects.filter(Q(
                    team = request.user.team) & Q(user = request.user))
        
        
            return render(request, 'expensense/approval_conditions.html',
                          {'conditions': conditions})
        
        else:
            return HttpResponse('You are not authorised for this page')


class SetApprovalConditions(View):
    """ Class to handle setting up Approval Conditions for expenses """

    @method_decorator(login_required)
    def get(self, request):
        """ Method to get the setApprovalConditions form"""
        if not request.user.role == 'EMP':
            # Only admin and manager can set approval conditions
            if request.user.role == 'ADM':
                form = ApprovalConditionForm(company=request.user.company)
                return render(request, 'expensense/set_approval_conditions.html',
                              {'form': form})

            elif request.user.role == 'MNG':
                form = ApprovalConditionForm(team=request.user.team)
                return render(request, 'expensense/set_approval_conditions.html',
                              {'form': form})

        else:
            return HttpResponse('You are not authorised in this section')

    @method_decorator(login_required)
    def post(self, request):
        """ Method to handle the submission of form"""
        form = ApprovalConditionForm(request.POST)

        if form.is_valid():
            # if form is valid get the company and team and create an
            # instance in ApprovalConditions table
            company = request.user.company
            team = Team.objects.get(id=request.POST.get('team'))
            ApprovalConditions.objects.get_or_create(company=company,
                                                     team=team,
                                                     user=request.user,
                                                     max_amount=request.POST.get('max_amount'))
            return redirect('expensense:set_approval_conditions')

        else:
            form_error = form.errors
            print(form.errors)
        # if form is not valid return the form and errors
        return render(request, 'expensense/expensense/set_approval_conditions.html', {'form': form, 'form_error': form_error})


class PendingRequestView(View):
    """ Class to handle pending expense request view """

    @method_decorator(login_required)
    def get(self, request):
        """ Method to handle the get request for pending expense requests"""

        # query the expense model and get those expenses that are pending for different roles

        if request.user.role == 'ADM':

            pending = Expense.objects.filter(Q(status=Expense.manager_approved) & Q(
                user_id__company=request.user.company)).order_by('-created_at')

        elif request.user.role == 'MNG':

            pending = Expense.objects.filter(Q(status=Expense.pending) & Q(
                user_id__team=request.user.team) & Q(
                user_id__company=request.user.company)).order_by('-created_at')

        else:

            pending = Expense.objects.filter(Q(status=Expense.pending) & Q(
                user_id=request.user)).order_by('-created_at')

        # paginate the objects received
        paginator = Paginator(pending, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'expensense/pending_expense_requests.html', {'page_obj': page_obj})


class ExpenseView(View):
    """ Class to handle expanded view of the expense"""

    @method_decorator(login_required)
    def get(self, request, expense_id):
        """ Method to handle the get request for expense view"""
        expense_details = get_object_or_404(Expense, id=expense_id)

        return render(request, 'expensense/expense_details.html', {'expense': expense_details})


class ApproveExpenseView(View):
    """ Class to handle manual approval of requests """

    @method_decorator(login_required)
    def get(self, request, expense_id):
        """ Method to approve """
        # approve the request based on user role

        expense_to_approve = get_object_or_404(Expense, id=expense_id)

        if request.user.role == 'MNG' and expense_to_approve.status == Expense.pending:
            # for manager set status as manager approved and the timestamp
            expense_to_approve.status = Expense.manager_approved
            expense_to_approve.manager_approved_at = timezone.now()
            expense_to_approve.manager_auto_approved = False
            expense_to_approve.save()

            return redirect('expensense:pending_exp_req')

        elif request.user.role == 'ADM' and expense_to_approve.status == Expense.manager_approved:
            # for admin set the status as admin approved and the timestamp
            expense_to_approve.status = Expense.admin_approved
            expense_to_approve.admin_approved_at = timezone.now()
            expense_to_approve.admin_auto_approved = False
            expense_to_approve.save()

            return redirect('expensense:pending_exp_req')

        else:
            return HttpResponse('Not Authorised')


class DenyExpenseView(View):
    """ Class to handle manual denial of requests """

    @method_decorator(login_required)
    def get(self, request, expense_id):
        """ Method to deny requests """

        expense_to_deny = get_object_or_404(Expense, id=expense_id)

        if request.user.role == 'MNG' and expense_to_deny.status == Expense.pending:
            # for manager set the status as manager rejected
            expense_to_deny.status = Expense.rejected_manager
            expense_to_deny.manager_auto_approved = False
            expense_to_deny.save()

            return redirect('expensense:pending_exp_req')

        elif request.user.role == 'ADM' and expense_to_deny.status == Expense.manager_approved:
            # for admin set the status as admin rejected
            expense_to_deny.status = Expense.rejected_admin
            expense_to_deny.admin_auto_approved = False
            expense_to_deny.save()

            return redirect('expensense:pending_exp_req')

        else:
            return HttpResponse('Not Authorised')


class GenerateExpensePDFView(View):
    """ Class to generate a downloadable pdf of Expenses """    

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """ Method to handle the get request of the """
        if kwargs:
            return self.generate_monthly_expense_pdf(request, *args, **kwargs)
        else:
            form = GeneratePdfForm
            return render(request, 'expensense/expense_pdf_form.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        """ Method to handle the post of the form """

        form = GeneratePdfForm(request.POST)

        if form.is_valid():
            # for valid form get the start and end date and generate the pdf
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            response = generate_pdf(request, start_date, end_date)

            return response

        return self.get(request)

    def generate_monthly_expense_pdf(self, request, *args, **kwargs):
        """ Method to get the monthly expense pdf"""
        start_date_str = kwargs.get('start_date')
        end_date_str = kwargs.get('end_date')

        # Convert start_date and end_date from string to datetime objects
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

        response = generate_pdf(request, start_date, end_date)

        return response


class BudgetView(View):
    """ Class to get budget for users """

    @method_decorator(login_required)
    def get(self, request):
        """ Method to get the existing budget """
        if not request.user.role == 'EMP':
            if request.user.role == 'ADM':
                budget = Company.objects.get(id=request.user.company.id)
            elif request.user.role == 'MNG':
                budget = Team.objects.get(id= request.user.team.id)


            return render(request, 'expensense/budget.html',
                          {'budget': budget})
        
        else:
            return HttpResponse('You are not authorised for this page')