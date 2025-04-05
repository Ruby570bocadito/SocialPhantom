import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import formataddr
import ssl
import json
from pathlib import Path
from typing import Dict, List, Optional
from queue import Queue
from threading import Thread
import time
import random
import string

class EmailSender:
    def __init__(self, config_file='config/email_config.json', max_threads=5):
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config(config_file)
        self.ssl_context = ssl.create_default_context()
        self.email_queue = Queue()
        self.threads = []
        self.max_threads = max_threads
        self.running = False
        self._start_workers()

    def _load_config(self, config_file):
        """Load email configuration from JSON file"""
        try:
            with open(config_file) as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load email config: {e}")
            return None

    def _start_workers(self):
        """Start email worker threads"""
        if not self.config:
            return
            
        self.running = True
        for _ in range(self.max_threads):
            thread = Thread(target=self._worker, daemon=True)
            thread.start()
            self.threads.append(thread)

    def _worker(self):
        """Worker thread that processes emails from queue"""
        while self.running or not self.email_queue.empty():
            try:
                email_data = self.email_queue.get(timeout=1)
                self._send_email(**email_data)
                self.email_queue.task_done()
            except Exception as e:
                self.logger.error(f"Email worker error: {e}")
                time.sleep(1)

    def send_phishing_email(self, template_file: str, recipient: str, 
                          campaign_name: Optional[str] = None,
                          variables: Optional[Dict] = None,
                          attachments: Optional[List[str]] = None) -> bool:
        """Send a phishing email with template variables and attachments"""
        if not self.config:
            self.logger.error("Email configuration not loaded")
            return False

        try:
            # Load and process template
            with open(template_file) as f:
                html_content = f.read()

            # Apply template variables
            if variables:
                for key, value in variables.items():
                    html_content = html_content.replace(f"{{{{{key}}}}}", str(value))

            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = formataddr((self.config['sender_name'], self.config['sender_email']))
            msg['To'] = recipient
            msg['Subject'] = self._generate_subject(campaign_name)

            # Add tracking if campaign specified
            if campaign_name:
                tracking_pixel = f'<img src="http://tracker.example.com/{campaign_name}/{hashlib.md5(recipient.encode()).hexdigest()}.png" width="1" height="1">'
                html_content = html_content.replace('</body>', f'{tracking_pixel}</body>')

            # Attach HTML content
            msg.attach(MIMEText(html_content, 'html'))

            # Add attachments
            if attachments:
                for attachment in attachments:
                    with open(attachment, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=Path(attachment).name)
                        part['Content-Disposition'] = f'attachment; filename="{Path(attachment).name}"'
                        msg.attach(part)

            # Queue email for sending
            self.email_queue.put({
                'msg': msg,
                'recipient': recipient,
                'campaign_name': campaign_name
            })

            return True

        except Exception as e:
            self.logger.error(f"Failed to prepare email: {e}", exc_info=True)
            return False

    def _send_email(self, msg, recipient, campaign_name):
        """Actually send the email (called by worker thread)"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with smtplib.SMTP_SSL(self.config['smtp_server'],
                                    self.config['smtp_port'],
                                    context=self.ssl_context) as server:
                    server.login(self.config['username'], self.config['password'])
                    server.send_message(msg)
                self.logger.info(f"Sent email to {recipient} (campaign: {campaign_name})")
                return
            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"Failed to send email to {recipient} after {max_retries} attempts: {e}")
                else:
                    time.sleep(2 ** attempt)  # Exponential backoff

    def _generate_subject(self, campaign_name: Optional[str]) -> str:
        """Generate a randomized email subject"""
        if not campaign_name:
            return self.config.get('subject', 'Important Notification')
            
        subjects = {
            'phishing': [
                f"Important: Your {campaign_name} account requires attention",
                f"Action required: {campaign_name} security update",
                f"Urgent: Verify your {campaign_name} credentials"
            ],
            'vishing': [
                f"Your {campaign_name} subscription is expiring",
                f"Immediate action required for {campaign_name}",
                f"{campaign_name} account verification needed"
            ]
        }
        return random.choice(subjects.get(campaign_name.lower(), [self.config.get('subject', 'Important Notification')]))

    def validate_email_config(self):
        """Test email configuration"""
        if not self.config:
            return False
        try:
            with smtplib.SMTP_SSL(self.config['smtp_server'],
                                self.config['smtp_port'],
                                context=self.ssl_context) as server:
                server.login(self.config['username'], self.config['password'])
            return True
        except Exception as e:
            self.logger.error(f"Email config validation failed: {e}")
            return False

    def __del__(self):
        """Clean up worker threads"""
        self.running = False
        for thread in self.threads:
            thread.join()
