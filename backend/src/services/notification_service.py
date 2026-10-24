from twilio.rest import Client
from src.core.config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_SMS_NUMBER,
    TWILIO_WA_NUMBER,
    FARMER_PHONE_NUMBER,
)


def send_notification(message_body: str) -> bool:
    """
    Dispatches SMS and WhatsApp alert notifications via Twilio REST API.
    Returns True if successfully sent, False otherwise.
    """
    try:
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            print("Twilio credentials missing in configuration.")
            return False

        if not FARMER_PHONE_NUMBER or not TWILIO_SMS_NUMBER:
            print("Twilio phone numbers missing in configuration.")
            return False

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        # 1. Send SMS
        client.messages.create(
            body=message_body,
            from_=TWILIO_SMS_NUMBER,
            to=FARMER_PHONE_NUMBER,
        )

        # 2. Send WhatsApp (if configured)
        if TWILIO_WA_NUMBER:
            try:
                client.messages.create(
                    body=message_body,
                    from_=f"whatsapp:{TWILIO_WA_NUMBER}",
                    to=f"whatsapp:{FARMER_PHONE_NUMBER}",
                )
            except Exception as wa_err:
                print(f"Twilio WhatsApp Error: {wa_err}")

        return True
    except Exception as e:
        print(f"Twilio Notification Error: {e}")
        return False
