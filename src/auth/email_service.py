from ssl import create_default_context
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from ssl import create_default_context

from loguru import logger
from celery import Celery

from src.auth.config import (
    BODY_FOR_CONFIRM_EMAIL,
    EMAIL_PASSWORD,
    EMAIL_SENDER,
    BODY_FOR_RESET_PASSWORD,
)

celery = Celery("send_email", broker="redis://localhost:6379")


@celery.task
def send_confirm_reset_password(reset_code: str, email_receiver: str) -> None:
    logger.debug(f"Email на сброс пароля для {email_receiver}")
    body = BODY_FOR_RESET_PASSWORD.format(email_receiver, reset_code)

    msg = MIMEText(body, "html")
    msg["FROM"] = EMAIL_SENDER
    msg["TO"] = email_receiver
    msg["SUBJECT"] = "Сброс пароля"

    context = create_default_context()

    with SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, email_receiver, msg.as_string())


@celery.task
def send_confirm_email(user_id: str, email_receiver: str) -> None:
    logger.debug(f"Email на верификацию для {email_receiver} с {user_id}")
    body = BODY_FOR_CONFIRM_EMAIL.format(user_id, user_id)

    msg = MIMEText(body, "html")
    msg["FROM"] = EMAIL_SENDER
    msg["TO"] = email_receiver
    msg["SUBJECT"] = "Верификация почты"

    context = create_default_context()

    with SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.sendmail(EMAIL_SENDER, email_receiver, msg.as_string())
