from django.db import models
from django.contrib.auth.models import AbstractUser
import os


# Create your models here.

class Category(models.Model):
    """ Class to store categories created by Admin as well as default"""

    category_name = models.CharField(max_length=128)

    def __str__(self):
        return self.category_name
    
    @classmethod
    def create_default_categories(cls):
        default_categories = ['Travel', 'Accomodation', 'Food', 'Miscellaneous']
        for cat in default_categories:
            cls.objects.get_or_create(category_name = cat)


class Company(models.Model):
    # class to store company details
    company = models.CharField(max_length=128, blank=False, unique=True)
    company_budget = models.DecimalField(max_digits=10, decimal_places=2, )
    categories = models.ManyToManyField(Category, related_name='companies')


    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.company
    
    def add(self, category):
        self.categories.set(category)
    
    def delete(self, *args, **kwargs):
        # Before deleting the company, remove all related categories
        self.categories.clear()
        super().delete(*args, **kwargs)

class Team(models.Model):
    #class to store team detatils
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='teams')
    team_name = models.CharField(max_length=128, blank=False)
    team_budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Teams'


    def __str__(self):
        return self.team_name
    


def get_signature_image_upload_path(instance, filename):
    """ Method to set a folder location for uploaded files """
    user_folder = instance.username
    team_folder = instance.team.team_name if instance.team else 'NoTeam'
    company_folder = instance.company.company
    return os.path.join('signatures', company_folder, team_folder, user_folder, filename)

class User(AbstractUser):
    # class to store user details
    
    role_choices = [
        ('ADM', 'Admin'),
        ('MNG', 'Manager'),
        ('EMP', 'Employee'),
    ]
    role = models.CharField(max_length=3, choices=role_choices, default='EMP')
    company = models.ForeignKey(Company, on_delete= models.CASCADE, null=True, blank=True, related_name='users')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    signature = models.ImageField(upload_to=get_signature_image_upload_path, null=True, blank=True)


def get_image_upload_path(instance, filename):
    """ Method to set a folder location for uploaded files """
    user_folder = instance.user_id.username
    team_folder = instance.user_id.team.team_name if instance.user_id.team else 'NoTeam'
    company_folder = instance.user_id.company.company
    return os.path.join('receipts', company_folder, team_folder, user_folder, filename)

class Expense(models.Model):
    ''' class to store expense details'''

    pending = 0
    manager_approved = 1
    admin_approved = 2
    rejected_manager = 3
    rejected_admin = 4

    status_choice = (
        (pending, 'Pending'),
        (manager_approved, 'Manager Approved'),
        (admin_approved, 'Admin Approved'),
        (rejected_manager, 'Rejected by Manager'),
        (rejected_admin, 'Rejected by Admin')
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    expense_name = models.CharField(max_length=128)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_date = models.DateField()
    note = models.TextField(max_length=256, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    receipt = models.ImageField(upload_to=get_image_upload_path)
    status = models.IntegerField(choices= status_choice, default= pending)
    created_at = models.DateTimeField(auto_now_add=True)
    manager_approved_at = models.DateTimeField(null=True, blank=True)
    admin_approved_at = models.DateTimeField(null=True, blank=True)
    manager_auto_approved = models.BooleanField(default=False, null=True, blank=True)
    admin_auto_approved = models.BooleanField(default=False, blank= True, null=True)
    similarity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Expenses'
    
    def __str__(self):
        return f'{self.user_id} - {self.expense_name} - {self.status}'


class ApprovalConditions(models.Model):
    """ Class to store the approval conditions """
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='approval_conditions')
    team = models.ForeignKey(Team, on_delete= models.CASCADE, related_name='approval_conditions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approval_conditions')
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
