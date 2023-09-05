from django.contrib import admin
from expensense.models import *

# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    """ Class to show custom details for Companies"""
    list_display = ('id', 'company')

class UserAdmin(admin.ModelAdmin):
    """ Class to show custom details for users """
    list_display = ('id', 'username', 'company', 'team', 'role')

admin.site.register(Company, CompanyAdmin)
admin.site.register(Team)
admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(ApprovalConditions)