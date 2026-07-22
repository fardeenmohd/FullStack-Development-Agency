class NotificationService:
    def send_new_lead_notification(self, lead_details):
        """Send notification about a new lead."""
        self._send_notification("new_lead", lead_details)

    def send_transaction_status_update(self, transaction_id, status):
        """Send update on the status of a transaction."""
        self._send_notification("transaction_status", {"id": transaction_id, "status": status})

    def send_product_listing_update(self, product_id, details):
        """Send updates on a product listing."""
        self._send_notification("product_listing", {"id": product_id, "details": details})

    def _send_notification(self, notification_type, data):
        """Helper method to handle the actual sending of notifications."""
        # Logic to send notification based on type and data
        pass
