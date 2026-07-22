import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NotificationsUITest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:3000/notifications")

    def test_subscribe_to_event(self):
        driver = self.driver
        subscribe_button = self.find_element_by_id("subscribe-button")
        subscribe_button.click()

        event_dropdown = self.find_element_by_id("event-dropdown")
        event_dropdown.send_keys("New Release")
        event_dropdown.send_keys(Keys.RETURN)

        confirm_subscription = self.find_element_by_id("confirm-subscription")
        confirm_subscription.click()

        success_message = self.find_element_by_id("success-message")
        self.assertIn("Subscribed to New Release", success_message.text)

    def test_configure_preferences(self):
        driver = self.driver
        preferences_button = self.find_element_by_id("preferences-button")
        preferences_button.click()

        email_checkbox = self.find_element_by_id("email-checkbox")
        email_checkbox.click()

        save_preferences = self.find_element_by_id("save-preferences")
        save_preferences.click()

        success_message = self.find_element_by_id("success-message")
        self.assertIn("Preferences saved", success_message.text)

    def find_element_by_id(self, element_id):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, element_id))
        )

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
