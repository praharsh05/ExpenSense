from django.core.management.base import BaseCommand
from expensense.models import User, Expense, Category
from datetime import datetime, timedelta
import random
from expensense.signature_matching import calculate_similarity

class Command(BaseCommand):
    help = 'Populates expenses for the past 2 years'

    def handle(self, *args, **options):
        user = User.objects.get(id=10)
        categories = Category.objects.all()
        current_date = datetime.now()

        for _ in range(24):  # 2 years
            for _ in range(3):  # 3 expenses per month
                expense_name = "Expense " + str(random.randint(1, 100))
                amount = round(random.uniform(10, 500), 2)
                expense_date = current_date - timedelta(days=random.randint(1, 30))
                note = "Demo note for the expense"
                category = random.choice(categories)
                status = 0
                receipt_path = 'media/signature_test/signature_receipt_2.jpeg'
                similarity_score = calculate_similarity(receipt_path, user.signature.path)
                
                Expense.objects.create(
                    user_id=user,
                    expense_name=expense_name,
                    amount=amount,
                    expense_date=expense_date,
                    note=note,
                    category=category,
                    status=status,
                    receipt= 'receipts/Company1/Team1/Test1Employee2/signature_receipt_3.png',
                    similarity = similarity_score
                )
            
            current_date -= timedelta(days=30)  # Move back by a month
