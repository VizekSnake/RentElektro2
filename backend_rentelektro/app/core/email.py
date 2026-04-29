from __future__ import annotations

import logging
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Protocol

from app.core.config import get_settings

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class OutboundEmail:
    recipient: str
    subject: str
    text_body: str


class EmailSender(Protocol):
    def send(self, message: OutboundEmail) -> None: ...


class ConsoleEmailSender:
    def send(self, message: OutboundEmail) -> None:
        logger.info(
            "console_email_delivery to=%s subject=%s\n%s",
            message.recipient,
            message.subject,
            message.text_body,
        )


class SMTPEmailSender:
    def __init__(self) -> None:
        self.settings = get_settings()

    def send(self, message: OutboundEmail) -> None:
        if not self.settings.MAIL_FROM_EMAIL:
            raise RuntimeError("MAIL_FROM_EMAIL must be set when EMAIL_DELIVERY_MODE=smtp.")
        if not self.settings.SMTP_HOST:
            raise RuntimeError("SMTP_HOST must be set when EMAIL_DELIVERY_MODE=smtp.")

        email_message = EmailMessage()
        email_message["From"] = self._build_from_header()
        email_message["To"] = message.recipient
        email_message["Subject"] = message.subject
        email_message.set_content(message.text_body)

        smtp = self._open_connection()
        try:
            smtp.send_message(email_message)
        except Exception:
            logger.exception("smtp_email_delivery_failed recipient=%s", message.recipient)
            raise
        finally:
            smtp.quit()

    def _build_from_header(self) -> str:
        assert self.settings.MAIL_FROM_EMAIL is not None
        if self.settings.MAIL_FROM_NAME:
            return f"{self.settings.MAIL_FROM_NAME} <{self.settings.MAIL_FROM_EMAIL}>"
        return str(self.settings.MAIL_FROM_EMAIL)

    def _open_connection(self) -> smtplib.SMTP:
        assert self.settings.SMTP_HOST is not None
        if self.settings.SMTP_USE_SSL:
            smtp: smtplib.SMTP = smtplib.SMTP_SSL(
                self.settings.SMTP_HOST,
                self.settings.SMTP_PORT,
                timeout=10,
            )
        else:
            smtp = smtplib.SMTP(
                self.settings.SMTP_HOST,
                self.settings.SMTP_PORT,
                timeout=10,
            )
            if self.settings.SMTP_USE_TLS:
                smtp.starttls()

        if self.settings.SMTP_USERNAME and self.settings.SMTP_PASSWORD:
            smtp.login(self.settings.SMTP_USERNAME, self.settings.SMTP_PASSWORD)
        return smtp


def get_email_sender() -> EmailSender:
    settings = get_settings()
    if settings.EMAIL_DELIVERY_MODE == "smtp":
        return SMTPEmailSender()
    return ConsoleEmailSender()
