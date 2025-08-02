import os
from twilio.rest import Client

# Fetch credentials from environment variables set in your .env file
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

# Initialize the Twilio client
try:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
except Exception as e:
    client = None
    print(f"Twilio client failed to initialize. Check credentials. Error: {e}")


def send_analysis_sms(phone_number, farm_name, crop_type, recommendation):
    """
    Sends the analysis result via SMS to the farmer.
    """
    if not client:
        print("ERROR: Twilio client not initialized. Cannot send SMS.")
        return

    # Ensure the phone number is in the E.164 format for Twilio
    if not phone_number.startswith('+'):
        # This is a simple assumption for Nigerian numbers. Adjust if needed.
        phone_number = f"+{phone_number}"

    try:
        body_message = (f"SoilGenie Alert for '{farm_name}':\n\n"
                        f"For your {crop_type.capitalize()} crop, our analysis shows: {recommendation}\n\n"
                        f"Plan your activities accordingly.")

        message = client.messages.create(
            body=body_message,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"SMS sent successfully to {phone_number}. SID: {message.sid}")
        return True
    except Exception as e:
        # In a real app, you would log this error more robustly
        print(f"Error sending SMS to {phone_number}: {e}")
        return False