from django.dispatch import receiver
from django.db.models.signals import post_save
from expensense.models import Expense, ApprovalConditions
from django.utils import timezone


@receiver(post_save, sender=Expense)
def auto_approve_expense(sender, instance, **kwargs):
    """ Method to auto approve expense requests """
    # print('Auto Approved called')
    try:
        #query to get the manager and admin condition for the employee's team and company
        manager_condition = ApprovalConditions.objects.get(user__role = 'MNG',
                                                            team = instance.user_id.team,
                                                            company = instance.user_id.company)
        
        admin_condition = ApprovalConditions.objects.get(user__role = 'ADM',
                                                         team = instance.user_id.team,
                                                         company = instance.user_id.company)
        # approve the request if the expense amount is lesser than in approval
        #  condition and is pending and the signature similarity is more than 80%
        if (manager_condition and (float(instance.amount) <= manager_condition.max_amount)
             and (int(instance.status)==Expense.pending) and (float(instance.similarity)>80)):
            # Auto approve for manager
            instance.manager_approved_at = timezone.now()
            instance.manager_auto_approved = True
            instance.status = Expense.manager_approved
            instance.save()
            manager_condition = None
        # approve the request if the expense amount is lesser than in approval
        #  condition and is manager approved and the signature similarity is more than 80%
        elif (admin_condition and (int(instance.status) == Expense.manager_approved)
               and (float(instance.amount) <= admin_condition.max_amount) and 
               float(instance.similarity)>80):
            # Auto approve for admin
            instance.admin_approved_at = timezone.now()
            instance.admin_auto_approved = True
            instance.status = Expense.admin_approved
            instance.save()
            admin_condition=None
        
    except ApprovalConditions.DoesNotExist:
        pass
