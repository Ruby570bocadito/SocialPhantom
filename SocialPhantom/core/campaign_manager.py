import os
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from threading import Thread
from multiprocessing import Queue
from modules.web_cloner import WebCloner
from modules.email_sender import EmailSender

class CampaignManager:
    def __init__(self, base_dir: str = "campaigns"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.web_cloner = WebCloner()
        self.email_sender = EmailSender()
        self.active_campaigns = {}
        self.event_queue = Queue()
        self.monitor_thread = Thread(target=self._monitor_campaigns, daemon=True)
        self.monitor_thread.start()

    def _monitor_campaigns(self):
        """Background thread for real-time campaign monitoring"""
        while True:
            while not self.event_queue.empty():
                event = self.event_queue.get()
                self._process_event(event)
            time.sleep(1)

    def _process_event(self, event: Dict):
        """Process campaign events in real-time"""
        campaign = self.get_campaign(event['campaign'])
        if campaign:
            # Update stats based on event type
            if event['type'] == 'email_sent':
                campaign['stats']['emails_sent'] += 1
            elif event['type'] == 'click':
                campaign['stats']['clicks'] += 1
            elif event['type'] == 'credential':
                campaign['stats']['credentials_captured'] += 1
            elif event['type'] == 'bec_reply':
                campaign['stats']['bec_replies'] += 1
            elif event['type'] == 'bec_transfer':
                campaign['stats']['bec_transfers'] += 1
            
            # Calculate success rates
            total = campaign['stats']['emails_sent']
            successes = campaign['stats']['credentials_captured']
            if campaign['type'] == 'BEC':
                total = campaign['stats']['bec_replies']
                successes = campaign['stats']['bec_transfers']
            campaign['stats']['success_rate'] = successes / total if total > 0 else 0
            
            self._save_campaign(campaign)

    def create_campaign(self, name: str, campaign_type: str, config: Optional[Dict] = None) -> bool:
        """Create a new campaign with enhanced configuration"""
        campaign_path = self.base_dir / name
        try:
            campaign_path.mkdir()
            
            # Enhanced configuration
            default_config = {
                "name": name,
                "type": campaign_type,
                "created": datetime.now().isoformat(),
                "status": "draft",
                "targets": [],
                "stats": {
                "emails_sent": 0,
                "clicks": 0,
                "credentials_captured": 0,
                "bec_replies": 0,
                "bec_transfers": 0,
                "success_rate": 0.0,
                    "last_activity": None
                },
                "settings": {
                    "template": "default",
                    "language": "en",
                    "schedule": None
                }
            }
            
            if config:
                default_config.update(config)
            
            with open(campaign_path / "config.json", "w") as f:
                json.dump(default_config, f, indent=2)
                
            # Enhanced directory structure
            (campaign_path / "clones").mkdir()
            (campaign_path / "templates").mkdir()
            (campaign_path / "logs").mkdir()
            (campaign_path / "reports").mkdir()
            
            self.logger.info(f"Created enhanced campaign '{name}' ({campaign_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create campaign: {str(e)}", exc_info=True)
            return False

    def run_campaign(self, name: str, targets: List[Dict], template: str) -> bool:
        """Execute a campaign (phishing or BEC)"""
        campaign_path = self.base_dir / name
        if not campaign_path.exists():
            self.logger.error(f"Campaign '{name}' not found")
            return False
            
        try:
            # Load campaign config
            with open(campaign_path / "config.json") as f:
                config = json.load(f)
                
            # Update status
            config["status"] = "running"
            config["started"] = datetime.now().isoformat()
            
            # Send appropriate emails based on campaign type
            if config["type"] == "PHISHING":
                for target in targets:
                    if self.email_sender.send_phishing_email(template, target, name):
                        config["stats"]["emails_sent"] += 1
                        self.event_queue.put({
                            "campaign": name,
                            "type": "email_sent",
                            "target": target
                        })
            elif config["type"] == "BEC":
                from modules.bec_simulator import BECSimulator
                bec = BECSimulator()
                for target in targets:
                    if bec.send_bec_email(template, target, target.get("spoofed_sender")):
                        config["stats"]["emails_sent"] += 1
                        self.event_queue.put({
                            "campaign": name,
                            "type": "email_sent",
                            "target": target
                        })
                    
            # Save updated config
            with open(campaign_path / "config.json", "w") as f:
                json.dump(config, f, indent=2)
                
            self.logger.info(f"Started phishing campaign '{name}' with {len(targets)} targets")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to run campaign: {e}")
            return False

    def get_campaign(self, name: str) -> Dict:
        """Retrieve campaign details"""
        campaign_path = self.base_dir / name
        if not campaign_path.exists():
            return None
            
        try:
            with open(campaign_path / "config.json") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load campaign: {e}")
            return None

    def list_campaigns(self) -> List[Dict]:
        """List all available campaigns"""
        campaigns = []
        for campaign_dir in self.base_dir.iterdir():
            if campaign_dir.is_dir():
                campaign = self.get_campaign(campaign_dir.name)
                if campaign:
                    campaigns.append(campaign)
        return campaigns
