from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Loan

@shared_task
def check_overdue_loans():
    today = date.today()
    overdue_loans = Loan.objects.filter(is_returned=False, due_date_lt=today)

    for loan in overdue_loans:
        member_email = loan.member.user.email
        book_title = loan.book.title

        send_mail(
            subject='Overdue Book Reminder',
            message=(
                f"Hello {loan.member.user.username}, \n\n"
                f"The book '{book_title}' is overdue. " 
                f"Your due date was {loan.due_date}. "
                f"Please return the book as soon as possible."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass
