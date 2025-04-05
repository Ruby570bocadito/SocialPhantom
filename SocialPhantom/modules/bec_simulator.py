import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from typing import List, Dict, Optional
from pathlib import Path
import json
from datetime import datetime

class BECSimulator:
    def __init__(self, config_path: str = "config/email_config.json"):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_path)
        self.templates_dir = Path("templates/bec")
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.tracking_data = {}  # Stores tracking information for each email
        self.tracking_server = None

    def _load_config(self, config_path: str) -> Dict:
        """Load email configuration"""
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            raise

    def _validate_template(self, template: str) -> bool:
        """Validate template exists"""
        template_path = self.templates_dir / f"{template}.html"
        return template_path.exists()

    def _create_message(self, template: str, target: Dict, sender_spoof: str) -> MIMEMultipart:
        """Create BEC email message with spoofed sender"""
        if not self._validate_template(template):
            raise ValueError(f"Invalid template: {template}")
            
        msg = MIMEMultipart()
        msg['From'] = sender_spoof
        msg['To'] = target['email']
        msg['Subject'] = target.get('subject', 'Urgent: Wire Transfer Required')
        
        with open(self.templates_dir / f"{template}.html") as f:
            body = f.read()
        
        # Personalize template with all target variables
        for key, value in target.items():
            body = body.replace(f'{{{{{key}}}}}', str(value))
        
        msg.attach(MIMEText(body, 'html'))
        return msg

    def send_bec_email(self, template: str, target: Dict, sender_spoof: str) -> bool:
        """Send BEC simulation email with spoofed sender"""
        try:
            message = self._create_message(template, target, sender_spoof)
            
            # Add tracking pixel
            tracking_pixel = f"<img src='http://localhost:8000/track/{target['email']}' style='display:none;'>"
            message.attach(MIMEText(tracking_pixel, 'html'))
            
            with smtplib.SMTP_SSL(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.login(self.config['username'], self.config['password'])
                server.send_message(message)
            
            # Initialize tracking data
            self.tracking_data[target['email']] = {
                'sent_time': datetime.now(),
                'opened': False,
                'replied': False,
                'forwarded': False,
                'attachments_opened': 0
            }
            
            self.logger.info(f"Sent BEC email to {target['email']} spoofing {sender_spoof}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send BEC email: {e}")
            return False

    def get_tracking_data(self, email: str) -> Optional[Dict]:
        """Get tracking data for a specific email"""
        return self.tracking_data.get(email)

    def start_tracking_server(self, port: int = 8000) -> bool:
        """Start the tracking server"""
        try:
            from .tracking_server import run_tracking_server
            import threading
            
            self.tracking_server = threading.Thread(
                target=run_tracking_server,
                args=(self.tracking_data, port),
                daemon=True
            )
            self.tracking_server.start()
            self.logger.info(f"Tracking server started on port {port}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start tracking server: {e}")
            return False

    def get_available_templates(self) -> List[str]:
        """List all available BEC templates"""
        return [f.stem for f in self.templates_dir.glob("*.html") 
                if f.is_file() and "[SECURITY TEST]" in f.read_text()]

    def create_template(self, name: str, content: str) -> bool:
        """Create new BEC email template"""
        try:
            with open(self.templates_dir / f"{name}.html", "w") as f:
                f.write(content)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create template: {e}")
            return False
