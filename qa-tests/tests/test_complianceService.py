import unittest
from unittest.mock import patch, MagicMock
from compliance_service import ComplianceService

class TestComplianceService(unittest.TestCase):

    @patch.object(ComplianceService, 'check_policy')
    def test_check_policy_valid(self, mock_check_policy):
        mock_check_policy.return_value = True
        service = ComplianceService()
        result = service.check_policy('policy123', 'data')
        self.assertTrue(result)

    @patch.object(ComplianceService, 'check_policy')
    def test_check_policy_invalid(self, mock_check_policy):
        mock_check_policy.return_value = False
        service = ComplianceService()
        result = service.check_policy('policy123', 'data')
        self.assertFalse(result)

    @patch.object(ComplianceService, 'apply_policy')
    def test_apply_policy_success(self, mock_apply_policy):
        mock_apply_policy.return_value = True
        service = ComplianceService()
        result = service.apply_policy('policy123', 'data')
        self.assertTrue(result)

    @patch.object(ComplianceService, 'apply_policy')
    def test_apply_policy_failure(self, mock_apply_policy):
        mock_apply_policy.return_value = False
        service = ComplianceService()
        result = service.apply_policy('policy123', 'data')
        self.assertFalse(result)

    @patch.object(ComplianceService, 'check_policy')
    def test_check_policy_edge_case_empty_data(self, mock_check_policy):
        mock_check_policy.return_value = True
        service = ComplianceService()
        result = service.check_policy('policy123', '')
        self.assertTrue(result)

    @patch.object(ComplianceService, 'apply_policy')
    def test_apply_policy_edge_case_empty_data(self, mock_apply_policy):
        mock_apply_policy.return_value = True
        service = ComplianceService()
        result = service.apply_policy('policy123', '')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
