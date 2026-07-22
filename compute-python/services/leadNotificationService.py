import os
from twilio.rest import Client

class LeadNotificationService:
    def __init__(self):
        self.twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

    def send_lead_status_update(self, lead_id, new_status):
        # Fetch lead data from the database
        lead_data = self.fetch_lead_data(lead_id)
        
        if not lead_data:
            print(f"Lead with ID {lead_id} not found.")
            return

        # Send notification using Twilio
        message = self.twilio_client.messages.create(
            body=f"Lead status updated to: {new_status}",
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=lead_data['phone_number']
        )

        print(f"Notification sent with SID: {message.sid}")

    def fetch_lead_data(self, lead_id):
        # Placeholder for database fetching logic
        # Replace this with actual database query
        leads = {
            '1': {'name': 'John Doe', 'phone_number': '+1234567890'},
            '2': {'name': 'Jane Smith', 'phone_number': '+0987654321'}
        }
        return leads.get(lead_id)
