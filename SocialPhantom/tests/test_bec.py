import unittest
import os
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from modules.bec_simulator import BECSimulator
from core.campaign_manager import CampaignManager

class TestBECSimulator(unittest.TestCase):
    def setUp(self):
        # Setup test environment
        self.test_dir = Path("tests/bec_test")
        self.test_dir.mkdir(exist_ok=True)
        
        # Create test config
        self.config_path = self.test_dir / "email_config.json"
        with open(self.config_path, "w") as f:
            json.dump({
                "smtp_server": "smtp.test.com",
                "smtp_port": 465,
                "username": "test@test.com",
                "password": "test123"
            }, f)
        
        # Create test template
        self.template_dir = self.test_dir / "templates/bec"
        self.template_dir.mkdir(parents=True, exist_ok=True)
        with open(self.template_dir / "test_template.html", "w") as f:
            f.write("<html>Test template {{target_name}} {{amount}} {{account}}</html>")

    def tearDown(self):
        # Clean up test environment
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @patch('smtplib.SMTP_SSL')
    def test_send_bec_email(self, mock_smtp):
        # Setup mock SMTP
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        # Test BEC email
        bec = BECSimulator(str(self.config_path))
        target = {
            "email": "target@example.com",
            "name": "John Doe",
            "amount": "$10,000",
            "account": "1234-5678"
        }
        
        result = bec.send_bec_email("test_template", target, "ceo@company.com")
        self.assertTrue(result)
        mock_server.login.assert_called_once()
        mock_server.send_message.assert_called_once()

    def test_bec_campaign_events(self):
        # Test campaign manager integration
        cm = CampaignManager(str(self.test_dir / "campaigns"))
        campaign_name = "test_bec_campaign"
        
        # Create BEC campaign
        self.assertTrue(cm.create_campaign(campaign_name, "BEC"))
        
        # Simulate BEC events
        cm.event_queue.put({
            "campaign": campaign_name,
            "type": "email_sent"
        })
        cm.event_queue.put({
            "campaign": campaign_name,
            "type": "bec_reply"
        })
        cm.event_queue.put({
            "campaign": campaign_name,
            "type": "bec_transfer"
        })
        
        # Allow time for event processing
        import time
        time.sleep(1.5)
        
        # Verify stats
        campaign = cm.get_campaign(campaign_name)
        self.assertEqual(campaign['stats']['emails_sent'], 1)
        self.assertEqual(campaign['stats']['bec_replies'], 1)
        self.assertEqual(campaign['stats']['bec_transfers'], 1)

if __name__ == '__main__':
    unittest.main()
