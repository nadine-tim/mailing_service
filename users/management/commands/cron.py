from datetime import datetime

import pytz
import smtplib
from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand

from customer.models import Customer
from mailing.models import Mailing, Log

""" Команда для отправки рассылки """
class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status=2)

        tz = pytz.timezone('Europe/Moscow')

        for new_mailing in mailings:
            customers = [customer.email for customer in Customer.objects.filter(user=new_mailing.user)]
            if new_mailing.mailing_time >= datetime.now(tz):
                mail_subject = new_mailing.message.body if new_mailing.message is not None else 'Рассылка'
                message = new_mailing.message.theme if new_mailing.message is not None else 'Вам назначена рассылка'
                try:
                    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, customers)
                    log = Log.objects.create(date_attempt=datetime.now(tz), status='Успешно', answer='200')
                    log.save()
                except smtplib.SMTPException as err:
                    log = Log.objects.create(date_attempt=datetime.now(tz), status='Ошибка', answer=err)
                    log.save()
                    # raise err
                new_mailing.status = 3
                new_mailing.save()