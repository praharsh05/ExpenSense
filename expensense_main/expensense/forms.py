
from django import forms
from expensense.models import *
from django.forms import Select


class Step1Form(forms.ModelForm):
    # Step-1 form
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    role_choices = [
        ('ADM', 'Admin'),
        ('MNG', 'Manager'),
        ('EMP', 'Employee'),
    ]
    role = forms.ChoiceField(choices=role_choices, widget=forms.Select(attrs={
        'class': 'form-select'}))
    signature = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'first_name', 'last_name', 'role', 'signature',)


class Step2FormAdmin(forms.ModelForm):
    # Step-2 form for admin
    company = forms.CharField(max_length=128)
    company_budget = forms.FloatField(max_value=100000000)
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
                                                widget= forms.CheckboxSelectMultiple, required = False)

    class Meta:
        model = Company
        fields = ('company', 'company_budget', 'categories')


class Step2FormManager(forms.ModelForm):
    # Step-2 form for manager
    company = forms.ModelChoiceField(queryset=Company.objects.all(),
                                      empty_label='Select Company', 
                                      widget=forms.Select(attrs={
                                          'class': 'form-select'}))
    team_name = forms.CharField(max_length=128)
    team_budget = forms.FloatField(max_value=100000000)

    def clean(self):
        return super().clean()

    class Meta:
        model = Team
        fields = ('company', 'team_name', 'team_budget', )


class Step2FormEmployee(forms.ModelForm):
    ''' Step-2 form for employee '''
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(), empty_label='Select Company', label='Company',
        widget=forms.Select(attrs={'class': 'form-select'}))
    team_name = forms.ModelChoiceField(queryset=Team.objects.all(),
                                        label='Team Name', required=False, 
                                        empty_label='Select Team',
                                        widget=forms.Select(attrs={'class': 'form-select'}))

    def clean(self):
        return super().clean()

    class Meta:
        model = User
        fields = ('company', 'team_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_name'].queryset = Team.objects.none()

        if 'company' in self.data:
            try:
                company_id = int(self.data.get('company'))
                self.fields['team_name'].queryset = Team.objects.filter(
                    company_id=company_id).order_by('team_name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty team queryset
        elif self.instance.pk:
            self.fields['team_name'].queryset = self.instance.company.team_name_set.order_by('team_name')


class ExpenseForm(forms.ModelForm):
    ''' class to get expense log from users'''
    expense_name = forms.CharField(max_length=128)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    expense_date = forms.DateField()
    category = forms.ModelChoiceField(queryset=Company.objects.none(),empty_label='Select Category', 
                                      widget=forms.Select(attrs={
                                          'class': 'form-select'}))
    note = forms.CharField(max_length=256, required=False)
    receipt = forms.ImageField()

    class Meta:
        model = Expense
        fields = ('expense_name', 'amount', 'expense_date', 'note', 'receipt', 'category')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ExpenseForm, self).__init__(*args, **kwargs)
        
        # Filter the categories based on the user's company
        if user and user.company:
            self.fields['category'].queryset = Category.objects.filter(companies=user.company)

class ApprovalConditionForm(forms.ModelForm):
    """ Class to set approval conditions """
    
    class Meta:
        model = ApprovalConditions
        fields = ('team', 'max_amount')
        widgets = {
            'team': Select(attrs={
                'class': 'form-select',
            })
        }
    
    def __init__(self, *args, **kwargs):
        company_id = kwargs.pop('company', None)
        team = kwargs.pop('team', None)
        # print('company_id: ', company_id)
        super(ApprovalConditionForm, self).__init__(*args, **kwargs)
        if team:
            self.fields['team'].queryset = Team.objects.filter(id=team.id)
        if company_id:
            self.fields['team'].queryset = Team.objects.filter(company=company_id)


class GeneratePdfForm(forms.Form):
    """ Form to handle start and end date for pdf generation"""

    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type':'date'}))