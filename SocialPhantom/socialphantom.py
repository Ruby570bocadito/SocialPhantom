#!/usr/bin/env python3
import argparse
import os
import logging
import json
from datetime import datetime
from typing import Optional
from enum import Enum, auto

class CampaignType(Enum):
    PHISHING = auto()
    VISHING = auto()
    SMISHING = auto()
    USB = auto()
    QR = auto()
    SOCIAL_MEDIA = auto()
    BEC = auto()
    MULTISTAGE = auto()
    WIFI = auto()
    DOCUMENT = auto()
    OSINT = auto()
    METADATA = auto()

# Advanced logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('socialphantom.log'),
        logging.StreamHandler()
    ]
)
VERSION = "1.0.0"

def create_campaign(name: str, campaign_type: CampaignType, config: Optional[dict] = None) -> bool:
    """Create a new campaign with enhanced directory structure"""
    try:
        campaign_path = f"campaigns/{name}"
        os.makedirs(campaign_path, exist_ok=True)
        
        # Default enhanced configuration
        default_config = {
            'name': name,
            'type': campaign_type.name,
            'created': datetime.now().isoformat(),
            'status': 'draft',
            'targets': [],
            'schedule': None,
            'language': 'en',
            'stats': {
                'targets_reached': 0,
                'interactions': 0,
                'success_rate': 0.0
            }
        }
        
        # Merge with provided config
        if config:
            default_config.update(config)
        
        # Save config
        with open(f"{campaign_path}/config.json", 'w') as f:
            json.dump(default_config, f, indent=2)
            
        # Create subdirectories
        os.makedirs(f"{campaign_path}/templates", exist_ok=True)
        os.makedirs(f"{campaign_path}/logs", exist_ok=True)
        os.makedirs(f"{campaign_path}/reports", exist_ok=True)
        
        logging.info(f"Created advanced campaign: {name} ({campaign_type.name})")
        return True
    except Exception as e:
        logging.error(f"Failed to create campaign: {str(e)}", exc_info=True)
        return False

def main():
    parser = argparse.ArgumentParser(
        description=f"SocialPhantom v{VERSION} - Advanced Cybersecurity Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Enhanced campaign commands
    campaign_parser = subparsers.add_parser('campaign', help='Manage advanced campaigns')
    campaign_subparsers = campaign_parser.add_subparsers(dest='action', required=True)
    
    # Create campaign
    create_parser = campaign_subparsers.add_parser('create', help='Create new campaign')
    create_parser.add_argument('--name', required=True, help='Campaign name')
    create_parser.add_argument('--type', 
                             choices=[t.name.lower() for t in CampaignType], 
                             required=True,
                             help='Campaign type')
    create_parser.add_argument('--language', default='en', help='Default language')
    create_parser.add_argument('--schedule', help='Schedule datetime (ISO format)')
    
    # List campaigns
    list_parser = campaign_subparsers.add_parser('list', help='List all campaigns')
    
    # Run campaign
    run_parser = campaign_subparsers.add_parser('run', help='Run existing campaign')
    run_parser.add_argument('--name', required=True, help='Campaign name to run')
    
    # Delete campaign
    del_parser = campaign_subparsers.add_parser('delete', help='Delete campaign')
    del_parser.add_argument('--name', required=True, help='Campaign name to delete')
    
    args = parser.parse_args()
    
    if args.command == 'campaign':
        if args.action == 'create':
            campaign_type = CampaignType[args.type.upper()]
            config = {
                'language': args.language,
                'schedule': args.schedule
            }
            create_campaign(args.name, campaign_type, config)

if __name__ == '__main__':
    main()
