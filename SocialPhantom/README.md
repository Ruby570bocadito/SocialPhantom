# SocialPhantom - Advanced Security Testing Framework

![SocialPhantom Logo](https://via.placeholder.com/150x50?text=SocialPhantom)

## ⚠️ Ethical Use Disclaimer
This tool is **strictly** for:
- Authorized penetration testing
- Security awareness training
- Defensive research

**Unauthorized use violates ethical guidelines and may be illegal.**

## 🚀 Core Features

### Campaign Management
- Multi-type campaigns (Phishing, BEC, Vishing, Smishing, USB, QR)
- Detailed statistics tracking including:
  - Email open rates
  - Click-through rates
  - BEC response metrics
- Scheduled execution
- Multi-language support

### Email System
- Template-based email generation
- Tracking pixel injection
- Attachment support
- Multi-threaded sending
- BEC-specific features:
  - Sender spoofing
  - Wire transfer templates
  - Financial request tracking

### Web Cloning
- Complete site mirroring
- Form modification
- Evasion techniques
- Asset management

## 🛠️ Installation

### Standard Installation
```bash
git clone https://github.com/yourrepo/SocialPhantom.git
cd SocialPhantom
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Kali Linux Specific
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required system packages
sudo apt install -y python3-pip python3-venv

# Clone and setup
git clone https://github.com/yourrepo/SocialPhantom.git
cd SocialPhantom
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Additional Kali tools that may be useful
sudo apt install -y seclists gobuster
```

## 🔧 Configuration

### Email Setup
1. Copy the example config file:
```bash
cp config/email_config.example.json config/email_config.json
```
2. Edit the config file with your SMTP credentials:
```json
{
    "smtp_server": "smtp.yourprovider.com",
    "smtp_port": 465,
    "username": "your_email@yourdomain.com",
    "password": "your_smtp_password",
    "sender_email": "no-reply@yourdomain.com",
    "sender_name": "Your Security Team"
}
```

### Campaign Templates
Store in `templates/` directory. Use `{{variable}}` syntax for dynamic content.

## 📚 Usage Examples

### Create a Campaign
```bash
# Phishing campaign
python socialphantom.py campaign create --name test --type phish --language en

# BEC campaign
python socialphantom.py campaign create --name bec_test --type bec --language en
```

### Run a Campaign
```bash
# Phishing campaign
python socialphantom.py campaign run --name test

# BEC campaign (requires targets file)
python socialphantom.py campaign run --name bec_test --targets targets.json
```

### Clone a Website
```python
from modules.web_cloner import WebCloner
cloner = WebCloner()
cloner.clone_site("https://example.com", "clones/example")
```

## 🛡️ Security Best Practices
1. Always use dedicated test accounts
2. Never use real credentials
3. Isolate testing environments
4. Obtain explicit consent
5. Regularly rotate credentials

## 🐛 Troubleshooting

### Email Issues
- Verify SMTP settings
- Check firewall rules
- Test SMTP connection:
```bash
python -c "import smtplib; smtplib.SMTP_SSL('smtp.example.com', 465).ehlo()"
```

### Web Cloning
- Check target site's robots.txt
- Verify network connectivity
- Review browser console for errors

## 📜 License
MIT License - See [LICENSE](LICENSE) for details

## 📧 Contact
security-team@example.com
