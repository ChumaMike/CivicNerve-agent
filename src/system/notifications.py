"""
SMS notifications via Africa's Talking — SA-focused, cheaper than Twilio for ZA numbers.
Configure AT_USERNAME and AT_API_KEY in your .env file.
Use AT_USERNAME=sandbox and any AT_API_KEY for development/testing.
"""
import os
from src.system.logger import get_logger

logger = get_logger(__name__)

AT_USERNAME = os.getenv("AT_USERNAME", "sandbox")
AT_API_KEY = os.getenv("AT_API_KEY", "")


def send_ticket_confirmation(phone: str, ticket_id: str, department: str):
    """Sends an SMS confirmation to the citizen after a report is submitted."""
    if not AT_API_KEY:
        logger.warning("Africa's Talking API key not configured; skipping SMS.")
        return

    try:
        import africastalking
        africastalking.initialize(username=AT_USERNAME, api_key=AT_API_KEY)
        sms = africastalking.SMS

        # Normalize ZA number format
        normalized = phone.strip()
        if normalized.startswith("0") and len(normalized) == 10:
            normalized = f"+27{normalized[1:]}"
        elif not normalized.startswith("+"):
            normalized = f"+27{normalized}"

        message = (
            f"CivicNerve: Your report {ticket_id} has been confirmed. "
            f"The {department} team will respond within 48 hours. "
            f"Track your report at civicnerve.co.za/{ticket_id}"
        )

        sms.send(message=message, recipients=[normalized])
        logger.info("SMS sent", extra={"ticket_id": ticket_id, "phone": normalized})

    except Exception as e:
        logger.warning("SMS delivery failed", extra={"ticket_id": ticket_id, "error": str(e)})


def send_status_update(phone: str, ticket_id: str, status: str, crew: str = None):
    """Sends an SMS when a report status changes (e.g., crew dispatched)."""
    if not AT_API_KEY:
        return

    try:
        import africastalking
        africastalking.initialize(username=AT_USERNAME, api_key=AT_API_KEY)
        sms = africastalking.SMS

        normalized = phone.strip()
        if normalized.startswith("0") and len(normalized) == 10:
            normalized = f"+27{normalized[1:]}"

        crew_info = f" Crew: {crew}." if crew else ""
        message = (
            f"CivicNerve Update: Ticket {ticket_id} status changed to {status}.{crew_info}"
        )

        sms.send(message=message, recipients=[normalized])
        logger.info("Status SMS sent", extra={"ticket_id": ticket_id, "status": status})

    except Exception as e:
        logger.warning("Status SMS failed", extra={"ticket_id": ticket_id, "error": str(e)})
