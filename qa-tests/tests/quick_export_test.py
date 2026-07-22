import unittest
from unittest.mock import patch
from your_module import QuickExport

class TestQuickExport(unittest.TestCase):
    @patch('your_module.YourClass.open_modal')
    def test_open_modal(self, mock_open_modal):
        quick_export = QuickExport()
        quick_export.open_button.click()
        mock_open_modal.assert_called_once()

    @patch('your_module.YourClass.select_leads')
    def test_select_leads(self, mock_select_leads):
        quick_export = QuickExport()
        leads = ['lead1', 'lead2']
        quick_export.select_leads(leads)
        mock_select_leads.assert_called_once_with(leads)

    @patch('your_module.YourClass.initiate_transaction')
    def test_initiate_transaction(self, mock_initiate_transaction):
        quick_export = QuickExport()
        quick_export.initiate_button.click()
        mock_initiate_transaction.assert_called_once()

if __name__ == '__main__':
    unittest.main()
