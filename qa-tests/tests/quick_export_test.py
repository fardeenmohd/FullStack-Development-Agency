import unittest
from unittest.mock import patch
from your_module import QuickExport

class TestQuickExport(unittest.TestCase):
    @patch('your_module.YourClass.open_modal')
    def test_open_modal(self, mock_open_modal):
        # Create an instance of QuickExport and simulate a button click to open the modal
        quick_export = QuickExport()
        quick_export.open_button.click()
        # Assert that the open_modal method was called once
        mock_open_modal.assert_called_once()

    @patch('your_module.YourClass.select_leads')
    def test_select_leads(self, mock_select_leads):
        # Create an instance of QuickExport and simulate selecting leads
        quick_export = QuickExport()
        leads = ['lead1', 'lead2']
        quick_export.select_leads(leads)
        # Assert that the select_leads method was called once with the provided leads
        mock_select_leads.assert_called_once_with(leads)

    @patch('your_module.YourClass.initiate_transaction')
    def test_initiate_transaction(self, mock_initiate_transaction):
        # Create an instance of QuickExport and simulate a button click to initiate a transaction
        quick_export = QuickExport()
        quick_export.initiate_button.click()
        # Assert that the initiate_transaction method was called once
        mock_initiate_transaction.assert_called_once()

if __name__ == '__main__':
    unittest.main()
