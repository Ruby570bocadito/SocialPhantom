# SocialPhantom API Reference

## Core Modules

### EmailSender (`modules/email_sender.py`)
```python
class EmailSender:
    def __init__(self, config_file='config/email_config.json', max_threads=5):
        """Initialize email sender with config and threading"""

    def send_phishing_email(self, template_file: str, recipient: str, 
                          campaign_name: Optional[str] = None,
                          variables: Optional[Dict] = None,
                          attachments: Optional[List[str]] = None) -> bool:
        """Send templated email with tracking"""
```

### WebCloner (`modules/web_cloner.py`)
```python
class WebCloner:
    def clone_site(self, url: str, output_dir: str, 
                  campaign_name: Optional[str] = None,
                  evasion_config: Optional[Dict] = None) -> bool:
        """Clone website with form modification"""
```

### CampaignManager (`core/campaign_manager.py`)
```python
class CampaignManager:
    def create_campaign(self, name: str, campaign_type: str, 
                      config: Optional[Dict] = None) -> bool:
        """Create new campaign with enhanced structure"""

    def run_campaign(self, name: str, 
                   targets: List[Dict], 
                   template: str) -> bool:
        """Execute campaign (phishing or BEC)
        
        For BEC campaigns, targets should include:
        {
          "email": "target@example.com",
          "name": "Target Name",
          "spoofed_sender": "ceo@company.com",
          "amount": "$50,000",
          "account": "XXXX-XXXX-XXXX"
        }
        """
```

## CLI Interface (`socialphantom.py`)
```bash
# Create campaign
python socialphantom.py campaign create --name test --type phish
python socialphantom.py campaign create --name bec_test --type bec

# List campaigns  
python socialphantom.py campaign list

# Run campaign
python socialphantom.py campaign run --name test
python socialphantom.py campaign run --name bec_test --targets targets.json
```

## Configuration Files

### Email Config (`config/email_config.json`)
```json
{
    "smtp_server": "smtp.example.com",
    "smtp_port": 465,
    "username": "your_email@example.com",
    "password": "your_password",
    "sender_email": "no-reply@example.com",
    "sender_name": "Security Team"
}
```

### Campaign Template (`templates/phishing_template.html`)
```html
<!-- Use {{variable}} for dynamic content -->
<a href="{{verification_link}}">Verify Account</a>
```

## Event Tracking
- `email_sent`: When email is successfully sent
- `click`: When target clicks a link  
- `credential`: When credentials are captured
- `bec_reply`: When target replies to BEC email
- `bec_transfer`: When target initiates wire transfer

## Error Handling
All modules provide detailed logging to `socialphantom.log`
